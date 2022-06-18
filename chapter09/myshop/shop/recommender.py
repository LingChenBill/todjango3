import redis
from django.conf import settings
from .models import Product

# 连接到redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender(object):
    """
    商品推荐类.
    存储购买的产品并检索给定产品的产品建议.
    """
    def get_product_key(self, id):
        """
        获取商品key.
        接收产品对象的ID，并为存储相关产品的已排序集生成Redis键，
        该键类似于Product：[ID]：purchased_with.
        :param id:
        :return:
        """
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        """
        接收一起购买的产品对象列表（即，属于同一订单）.
        :param products:
        :return:
        """
        products_ids = [p.id for p in products]

        # 再次迭代产品ID并跳过同一产品，以便获得与每个产品一起购买的产品.
        for product_id in products_ids:
            for with_id in products_ids:
                # 购买每种产品的其他产品.
                if product_id != with_id:
                    # 将排序集中包含的每个产品ID的分数递增为1.
                    # 分数代表另一种产品与给定产品一起购买的次数.
                    r.zincrby(self.get_product_key(product_id),
                              1,
                              with_id)

    def suggest_products_for(self, products, max_results=6):
        """
        检索为给定产品列表一起购买的产品.
        :param products: 这是要获取建议的产品对象列表. 它可以包含一个或多个产品.
        :param max_results: 这是一个表示最大数的整数返回的建议数量.
        :return:
        """
        product_ids = [p.id for p in products]
        # 只有一个产品时.
        if len(products) == 1:
            # 您检索了与给定产品一起购买，按一起购买的总次数订购.
            # 为此，可以使用Redis的ZRANGE命令.
            # 可以将结果数限制为max_results属性中指定的数目（默认为6）.
            suggestions = r.zrange(self.get_product_key(product_ids[0]),
                                   0,
                                   -1,
                                   desc=True)[:max_results]
        else:
            # 产生一个临时key.
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'

            # 将排序集中包含的项目的所有分数合并并求和每个给定产品的.
            # 这是使用Redis zunionstore完成的命令zunionstore命令执行排序集的并集
            # 并存储元素得分的聚合和在新的Redis的key中.
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)

            # 获得与您相同的产品正在获得的建议. 从生成的使用zrem命令对集合进行排序.
            # 删除推荐产品的ID.
            r.zrem(tmp_key, *product_ids)

            # 按分数、降序排序获取产品ID.
            suggestions = r.zrange(tmp_key,
                                   0,
                                   -1,
                                   desc=True)[:max_results]
            # 删除临时key.
            r.delete(tmp_key)
        
        suggested_products_ids = [int(id) for id in suggestions]
        # 获取建议产品并按订单顺序排序.
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))

        return suggested_products

    def clear_purchases(self):
        """
        清除产品推荐.
        :return:
        """
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
