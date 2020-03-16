from datetime import datetime
import logging
import  requests
from hashlib import md5
from time import sleep
from apscheduler.schedulers.background import BlockingScheduler,BackgroundScheduler
import  kzconfig 
import json

logging.basicConfig(
    handlers=[logging.FileHandler('log.log', 'a', 'utf-8')],
    level=logging.INFO,format='%(asctime)s %(levelname)s - %(message)s'
)

logger =logging.getLogger("kouzhao")

def token()->str:
    now = datetime.now()
    now_str = now.strftime("%Y*%m-%d")+ "_Qwe"
    m = md5()
    m.update(now_str.encode("utf-8"))
    url_md = m.hexdigest()[7:15]

    return  url_md


headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4078.0 Mobile Safari/537.36"
}




def miaosha_kz():
    form_data = kzconfig.form_data
    # form_data = {}
    sleep(1)
    url = "https://kzapi.****.gov.cn/kouzhao/sq/miaosha/"+token()
    logger.info("today url is %s"%url)

    for i in range(1,kzconfig.MAX_TRY_TIME+1):
        logger.info("开始第 %d 此尝试 "%(i))
        res =  requests.post(url=url,data=form_data,headers=headers,timeout=10)

        json_data = res.json()
        logger.info(json.dumps(json_data,ensure_ascii=False))
        shop_res = json_data.get("responseFlag","0") == "1"
        if shop_res:
            logger.info("第 %d 抢购成功"%i)
            break
        elif json_data.get("responseMessage","") == "您好，当前时间段口罩已经约完，建议关注后续的预约活动" :
            logger.info("当前时间段口罩已经约完")
            break
        elif json_data.get("status",200) == 404:
            break
        logger.info("第 %d 抢购失败 %f 秒后再次尝试" % (i,kzconfig.SLEEP_TIME))
        sleep(kzconfig.SLEEP_TIME)
    logger.info("抢购结束")

def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(miaosha_kz, 'cron'
                      , day="*/7", hour='19',minute="0",second='1'
                      ,timezone =kzconfig.cst_tz)
    scheduler.start()

if __name__ == '__main__':
    main()