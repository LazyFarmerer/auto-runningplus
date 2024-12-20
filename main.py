import os
from dotenv import load_dotenv

from res.site.runningplus import 러닝플러스


if __name__ == "__main__":
    load_dotenv()
    ID = os.getenv("RUNNINGPLUS_ID")
    PW = os.getenv("RUNNINGPLUS_PW")
    # 둘중 하나라도 없으면 종료
    if (ID is None) or (PW is None): quit()

    main = 러닝플러스("https://www.runningplus.net/Member/Login.nm", ID, PW)
    main.run()