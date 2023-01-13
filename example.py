def cal_per(line, time, line_stations, all_train_info):

    li_sum = []
    li_sit_per = []
    li_person_per = []
    li_per = []

    sum = 0  # 차량 내의 인원 초기화

    # 호선의 첫번째부터 연산
    for line_station in line_stations:

        # 주어진 호선과 역명에 맞는 데이터 시리즈 받아오기
        tmp = all_train_info[
            (all_train_info.station == line_station) & (all_train_info.subway == line)
        ]
        print(line_station, line)
        print(tmp)
        in_num = tmp[f"in_{time}"].item()  # 탑승인원
        out_num = tmp[f"out_{time}"].item()  # 하차인원
        in_tf_num = tmp[f"tf_in_{time}"].item()  # (환승 후) 탑승인원
        out_tf_num = tmp[f"tf_out_{time}"].item()  # (환승 후) 하차인원
        sit_cnt = tmp["sit_cnt"].item()  # 사용 가능한 좌석 수
        person_cnt = tmp["person_cnt"].item()  # 적정한 탑승 승객 인원 수

        # 차량 탑승시 앉아 갈 수 있는 확률

        if sum < 0:
            sum_tmp = 0  # 노선 전체를 계산 할 때는 오차를 허용할 수 있지만 인원을 파악하려면 음수가 나와서는 안됨
        else:
            sum_tmp = sum

        if tmp.if_tf.item():

            last = sum_tmp - out_num - out_tf_num  # 차량안에 남는사람

            if last < 0:
                last = 0

            can_sit = sit_cnt - last  # 남아있는 좌석 수

        else:
            last = sum_tmp - out_num  # 차량안에 남는사람

            if last < 0:
                last = 0

            can_sit = sit_cnt - last  # 남아있는 좌석 수

        if can_sit > 0:  # 앉아 갈 수 있는 좌석이 남았을 때
            sit_per = (can_sit / sit_cnt) * 100

        else:
            sit_per = 0

        # 차량 내부에 있는데 내 주변 의자가 비어있을 확률 (자리 순환률 [얼마나 사람들이 일어나서 나갈 것인가] )
        if sum_tmp <= 0:
            per = 100

        else:
            if tmp.if_tf.item():

                per = ((out_num + out_tf_num) / sum_tmp) * 100  # 차량안에 있는 사람이 나갈 확률

                if per > 100:
                    per = 100

            else:

                per = ((out_num) / sum_tmp) * 100  # 차량안에 있는 사람이 나갈 확률

                if per > 100:
                    per = 100

        # 현 역에서 차량에 탑승하고 있는 전체 인원 계산

        if tmp.if_tf.item():
            # 환승가능한 역의 갯수 받아오기
            transfer_cnt = tmp.tf_cnt.item()

            # 현재 타고있는 인원 계산 공식
            sum = sum + (in_num + in_tf_num - out_num - out_tf_num) / transfer_cnt

        else:
            # 현재 타고있는 인원 계산 공식
            sum = sum + in_num - out_num

        # 적정 탑승 인원과 비교한 차량 내부 혼잡도

        if sum < 0:
            person_per = 0

        else:
            person_per = (sum / person_cnt) * 100

        li_sum.append(sum)
        li_sit_per.append(sit_per)
        li_person_per.append(person_per)
        li_per.append(per)

    return {
        "sum": li_sum,
        "sit_per": li_sit_per,
        "person_per": li_person_per,
        "per": li_per,
    }


#################################################################################################
# line = 8            # 호선
# time = '12'         # 시간
# line_stations = ['암사', '천호(풍납토성)', '강동구청',
#                  '몽촌토성(평화의문)', '잠실(송파구청)',
#                  '석촌', '송파', '가락시장', '문정', '장지',
#                  '복정', '산성', '남한산성입구(성남법원.검찰청)',
#                  '단대오거리', '신흥', '수진', '모란']

#                     # 해당 호선의 순서


# print(cal_per(line, time, line_stations, all_train_info))
