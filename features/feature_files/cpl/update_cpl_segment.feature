##language: zh-CN
#功能: 我想修改一个cpl segment
#
#  场景大纲: 修改一个cpl segment
#    假如获取cpl访问地址
#    当修改cpl参数为  <cpl_update_json>和<success>
#    那么检查CPL 是否修改成功  <uuid>
#
#    例子:
#       | cpl_update_json   | success | uuid                                 |
#       | {"cpl_uuids": ["ab3eb01f-3c87-4e65-94d1-5aae1c9c4f8b"],"producer_credit_offset": 15200, "ratings":[] } | 200     | ab3eb01f-3c87-4e65-94d1-5aae1c9c4f8b |
##      | {"cpl_uuids": ["a9e827db-0353-4123-8c59-8a41bbab1d39"],"producer_credit_offset": 15200, "ratings":[] } | 200     | a9e827db-0353-4123-8c59-8a41bbab1d39 |
##      | {"cpl_uuids": ["57395cce-532d-4e6e-bf22-4a3bbed6bfea"] ,"ratings": [{"rating_key": "aamts.io/nating_value": "16","territory": "UK2"}]} | 200 s/local-rating","r    | 45e695fe-30fd-4410-a211-f18a56bf87ac |
#
#
