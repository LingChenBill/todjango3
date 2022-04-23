from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from .tasks import payment_completed
import braintree

# Create your views here.

# 实例化braintree的网关.
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    """
    支付流程.
    :param request:
    :return:
    """
    order_id = request.session.get('order_id')

    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # 取回付款方法.
        nonce = request.POST.get('payment_method_nonce', None)
        result = gateway.transaction.sale({
            'amount': f'{total_cost: .2f}',
            'payment_method_nonce': nonce,
            'options': {
                # 发送带有True的submit_for_settlement选项, 这样交易就会自动提交进行结算.
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            # 更新订单支付状态.
            order.paid = True
            # 保存交易id.
            order.braintree_id = result.transaction.id
            order.save()

            # 发送异步任务.
            payment_completed.delay(order.id)

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        client_token = gateway.client_token.generate()

        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    """
    支付完成.
    :param request:
    :return:
    """
    return render(request, 'payment/done.html')


def payment_canceled(request):
    """
    支付取消.
    :param request:
    :return:
    """
    return render(request, 'payment/canceled.html')
