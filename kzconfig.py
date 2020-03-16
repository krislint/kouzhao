from datetime import  datetime
from pytz import timezone

cst_tz = timezone('Asia/Shanghai')
MAX_TRY_TIME = 5
SLEEP_TIME = 2
form_data = {
    "name":"",
    "idNumber":"",
    "phone":"",
    "address":"",
    "phoneBackup":"",
    "addressDetail":"",
    "goodsCode":"",
    "addressCode":""
}
