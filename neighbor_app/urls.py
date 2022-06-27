from django.urls import path
from . import views

app_name = 'neighbor_app'
urlpatterns = [
    path('', views.TopListView.as_view(), name="top"),
    path('sell_form/', views.SellFormView.as_view(), name="sell_form"),
    path('sell_save/', views.SellSaveView.as_view(), name="sell_save"),
    path('merchandise_detail/<uuid:pk>/', views.MerchandiseDetailTestView.as_view(), name="merchandise_detail"),
    path('talk_list/', views.TalkListView.as_view(), name="talk_list"),
    path('about_service/', views.AboutServiceView.as_view(), name="about_service"),
    path('talk_room/<uuid:pk>/', views.TalkRoomView.as_view(), name="talk_room"),
    path('talk_room_post/', views.TalkRoomPostView.as_view(), name="talk_room_post"),
    path('sell_list/', views.SellListView.as_view(), name="sell_list"),
    path('pay/', views.PayView.as_view(), name="pay"),  # 新しいトークルーム作成、メール送信、商品情報更新
    path('account/', views.AccountView.as_view(), name="account"),
    path('account_edit/', views.AccountEditView.as_view(), name="account_edit"),
    # path('method_of_payment/', views.MethodOfPaymentView.as_view(), name="method_of_payment"),
    path('display_stop/', views.DisplayStopView.as_view(), name="display_stop"),
    path('merchandise_edit/<uuid:pk>/', views.MerchandiseEditView.as_view(), name="merchandise_edit"),
    path('merchandise_edit_post/', views.MerchandiseEditPostView.as_view(), name="merchandise_edit_post"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('information/', views.InformationView.as_view(), name="information"),
    path('information_detail/<uuid:pk>/', views.InformationDetailView.as_view(), name="information_detail"),
    path('retire/', views.RetireView.as_view(), name="retire"),  # 退会処理
    path('account_profile/<uuid:pk>/', views.AccountProfileView.as_view(), name="account_profile"),
    path('sctl/', views.SCTL.as_view(), name='sctl'),  # 特定商取引法に基づく通知
    path('terms_of_service/', views.TermsOfService.as_view(), name='terms_of_service'),  # 利用規約
    path('privacy_policy/', views.PrivacyPolicy.as_view(), name='privacy_policy'),  # プライバシーポリシー
    # path('card_register/', views.CardRegister.as_view(), name='card_register'),
    # path('card_delete/', views.CardDeleteView.as_view(), name="card_delete"),
    # path('card_update/', views.CardUpdateView.as_view(), name="card_update"),
    # path('refund_request/', views.RefundRequestView.as_view(), name="refund_request"),
    path('email_request/', views.EmailRequestView.as_view(), name="email_request"),  # メールの受け取り設定
    path('send_email/', views.SendEmailView.as_view(), name="send_email"),  # メールを一斉に送る機能（運営のみ）
    path('department_selections/', views.DepartmentSelectionsView.as_view(), name="department_selections"),  # sell_formに学部のリストを返す
    # path('sell_commission_history/', views.SellCommissionHistoryView.as_view(), name="sell_commission_history"),
    # path('refund_procedure/<uuid:pk>/', views.RefundProcedureView.as_view(), name="refund_procedure"),
    # path('refund_request_post/', views.RefundProcedurePost.as_view(), name="refund_request_post"),
    # path('talk_list_for_refund/', views.TalkListForRefund.as_view(), name="talk_list_for_refund"),
    path('check_username/', views.ajax_get_customuser, name='check_username'),  # 新規登録の際に既にユーザー名が存在するかを判定
]

