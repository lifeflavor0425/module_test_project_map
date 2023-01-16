# 모듈 가져오기
# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import re


"""# 서울시 1~9 호선 DF 병합"""


def make_DataFrame():
    #  1호선 ~ 9호선
    line_url = [
        "./station_line_urls/station_line1.xlsx",
        "./station_line_urls/station_line2.xlsx",
        "./station_line_urls/station_line3.xlsx",
        "./station_line_urls/station_line4.xlsx",
        "./station_line_urls/station_line5.xlsx",
        "./station_line_urls/station_line6.xlsx",
        "./station_line_urls/station_line7.xlsx",
        "./station_line_urls/station_line8.xlsx",
        "./station_line_urls/station_line9.xlsx",
    ]
    # DF 반환 함수
    def station_lines(url):
        line_df = pd.read_excel(url)
        columns = {"역사명": "station", "위도": "long", "경도": "lat", "호선": "subway"}
        line_df.rename(columns=columns, inplace=True)
        return line_df

    # 병합
    subway_crd = pd.concat(
        [station_lines(url) for url in line_url],
    )
    # 필요없는 컬럼 제거
    subway_crd = subway_crd.drop(
        columns=[
            "Unnamed: 0",
            "Unnamed: 0.1",
            "Unnamed: 0.1.1",
            "Unnamed: 0.1.1.1",
            # "Unnamed: 0.1.1.1.1",
            "Unnamed: 0.2",
            "역사_ID",
        ]
    )
    subway_crd["station"] = subway_crd["station"].apply(lambda x: re.sub(r"\([^)]*\)", "", x))

    # 환승역_환승인원정보 DF
    train_change = pd.read_csv(
        "./station_line_urls/환승역_환승인원정보_이수_20211231.csv", encoding="cp949"
    )
    train_change["역명"] = train_change["역명"].apply(lambda x: re.sub(r"\([^)]*\)", "", x))

    subway_crd["if_tf"] = subway_crd["station"].apply(
        lambda x: 1 if x in list(train_change["역명"]) else 0
    )
    subway_location = subway_crd
    subway_location = subway_location.reset_index()
    subway_location = subway_location.sort_values(by="index")
    subway_location.to_excel("./all_station_line.xlsx")
    return subway_location
