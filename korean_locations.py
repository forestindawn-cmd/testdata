"""
한국 지역 데이터베이스
한글 지역명과 영문 지역명을 매핑하고, 구/동 단위 검색을 지원합니다.
"""

# 서울특별시 구별 데이터
SEOUL_DISTRICTS = {
    # 강남구권
    "강남구": "Gangnam-gu, Seoul",
    "서초구": "Seocho-gu, Seoul", 
    "송파구": "Songpa-gu, Seoul",
    "강동구": "Gangdong-gu, Seoul",
    
    # 강북구권
    "강북구": "Gangbuk-gu, Seoul",
    "성북구": "Seongbuk-gu, Seoul",
    "동대문구": "Dongdaemun-gu, Seoul",
    "중랑구": "Jungnang-gu, Seoul",
    
    # 서북구권
    "은평구": "Eunpyeong-gu, Seoul",
    "서대문구": "Seodaemun-gu, Seoul",
    "마포구": "Mapo-gu, Seoul",
    
    # 서남구권
    "양천구": "Yangcheon-gu, Seoul",
    "강서구": "Gangseo-gu, Seoul",
    "구로구": "Guro-gu, Seoul",
    "금천구": "Geumcheon-gu, Seoul",
    "영등포구": "Yeongdeungpo-gu, Seoul",
    "동작구": "Dongjak-gu, Seoul",
    "관악구": "Gwanak-gu, Seoul",
    
    # 도심권
    "종로구": "Jongno-gu, Seoul",
    "중구": "Jung-gu, Seoul",
    "용산구": "Yongsan-gu, Seoul",
    
    # 동북구권
    "성동구": "Seongdong-gu, Seoul",
    "광진구": "Gwangjin-gu, Seoul",
    "노원구": "Nowon-gu, Seoul",
    "도봉구": "Dobong-gu, Seoul",
}

# 부산광역시 구별 데이터
BUSAN_DISTRICTS = {
    "중구": "Jung-gu, Busan",
    "서구": "Seo-gu, Busan",
    "동구": "Dong-gu, Busan",
    "영도구": "Yeongdo-gu, Busan",
    "부산진구": "Busanjin-gu, Busan",
    "동래구": "Dongnae-gu, Busan",
    "남구": "Nam-gu, Busan",
    "북구": "Buk-gu, Busan",
    "해운대구": "Haeundae-gu, Busan",
    "사하구": "Saha-gu, Busan",
    "금정구": "Geumjeong-gu, Busan",
    "강서구": "Gangseo-gu, Busan",
    "연제구": "Yeonje-gu, Busan",
    "수영구": "Suyeong-gu, Busan",
    "사상구": "Sasang-gu, Busan",
    "기장군": "Gijang-gun, Busan",
}

# 인천광역시 구별 데이터
INCHEON_DISTRICTS = {
    "중구": "Jung-gu, Incheon",
    "동구": "Dong-gu, Incheon",
    "미추홀구": "Michuhol-gu, Incheon",
    "연수구": "Yeonsu-gu, Incheon",
    "남동구": "Namdong-gu, Incheon",
    "부평구": "Bupyeong-gu, Incheon",
    "계양구": "Gyeyang-gu, Incheon",
    "서구": "Seo-gu, Incheon",
    "강화군": "Ganghwa-gun, Incheon",
    "옹진군": "Ongjin-gun, Incheon",
}

# 광역시/도 및 주요 시/군 데이터
KOREA_REGIONS = {
    # 광역시/특별시
    "서울": "Seoul",
    "서울특별시": "Seoul",
    "부산": "Busan", 
    "부산광역시": "Busan",
    "대구": "Daegu",
    "대구광역시": "Daegu", 
    "인천": "Incheon",
    "인천광역시": "Incheon",
    "광주": "Gwangju",
    "광주광역시": "Gwangju",
    "대전": "Daejeon", 
    "대전광역시": "Daejeon",
    "울산": "Ulsan",
    "울산광역시": "Ulsan",
    "세종": "Sejong",
    "세종특별자치시": "Sejong",
    
    # 경기도
    "수원": "Suwon",
    "성남": "Seongnam", 
    "고양": "Goyang",
    "용인": "Yongin",
    "부천": "Bucheon",
    "안산": "Ansan",
    "안양": "Anyang",
    "남양주": "Namyangju",
    "화성": "Hwaseong",
    "평택": "Pyeongtaek",
    "의정부": "Uijeongbu",
    "시흥": "Siheung",
    "파주": "Paju",
    "광명": "Gwangmyeong",
    "김포": "Gimpo",
    "군포": "Gunpo",
    "광주": "Gwangju-si",
    "이천": "Icheon",
    "양주": "Yangju",
    "오산": "Osan",
    "구리": "Guri",
    "안성": "Anseong",
    "포천": "Pocheon",
    "의왕": "Uiwang",
    "하남": "Hanam",
    "여주": "Yeoju",
    "양평": "Yangpyeong",
    "동두천": "Dongducheon",
    "과천": "Gwacheon",
    "가평": "Gapyeong",
    "연천": "Yeoncheon",
    
    # 강원도
    "춘천": "Chuncheon",
    "원주": "Wonju",
    "강릉": "Gangneung",
    "동해": "Donghae",
    "태백": "Taebaek",
    "속초": "Sokcho",
    "삼척": "Samcheok",
    
    # 충청북도
    "청주": "Cheongju",
    "충주": "Chungju",
    "제천": "Jecheon",
    
    # 충청남도
    "천안": "Cheonan",
    "공주": "Gongju",
    "보령": "Boryeong",
    "아산": "Asan",
    "서산": "Seosan",
    "논산": "Nonsan",
    "계룡": "Gyeryong",
    "당진": "Dangjin",
    
    # 전라북도
    "전주": "Jeonju",
    "군산": "Gunsan",
    "익산": "Iksan",
    "정읍": "Jeongeup",
    "남원": "Namwon",
    "김제": "Gimje",
    
    # 전라남도
    "목포": "Mokpo",
    "여수": "Yeosu",
    "순천": "Suncheon",
    "나주": "Naju",
    "광양": "Gwangyang",
    
    # 경상북도
    "포항": "Pohang",
    "경주": "Gyeongju",
    "김천": "Gimcheon",
    "안동": "Andong",
    "구미": "Gumi",
    "영주": "Yeongju",
    "영천": "Yeongcheon",
    "상주": "Sangju",
    "문경": "Mungyeong",
    "경산": "Gyeongsan",
    
    # 경상남도
    "창원": "Changwon",
    "마산": "Masan",
    "진주": "Jinju",
    "통영": "Tongyeong",
    "사천": "Sacheon",
    "김해": "Gimhae",
    "밀양": "Miryang",
    "거제": "Geoje",
    "양산": "Yangsan",
    
    # 제주특별자치도
    "제주": "Jeju",
    "서귀포": "Seogwipo",
}

# 주요 동 단위 지역 (서울 중심)
SEOUL_DONG_AREAS = {
    # 강남구
    "역삼동": "Yeoksam-dong, Gangnam-gu, Seoul",
    "삼성동": "Samsung-dong, Gangnam-gu, Seoul", 
    "논현동": "Nonhyeon-dong, Gangnam-gu, Seoul",
    "압구정동": "Apgujeong-dong, Gangnam-gu, Seoul",
    "청담동": "Cheongdam-dong, Gangnam-gu, Seoul",
    "신사동": "Sinsa-dong, Gangnam-gu, Seoul",
    "도곡동": "Dogok-dong, Gangnam-gu, Seoul",
    "개포동": "Gaepo-dong, Gangnam-gu, Seoul",
    
    # 서초구
    "서초동": "Seocho-dong, Seocho-gu, Seoul",
    "방배동": "Bangbae-dong, Seocho-gu, Seoul",
    "반포동": "Banpo-dong, Seocho-gu, Seoul",
    "잠원동": "Jamwon-dong, Seocho-gu, Seoul",
    "양재동": "Yangjae-dong, Seocho-gu, Seoul",
    "우면동": "Umyeon-dong, Seocho-gu, Seoul",
    
    # 송파구
    "잠실동": "Jamsil-dong, Songpa-gu, Seoul",
    "신천동": "Sincheon-dong, Songpa-gu, Seoul",
    "석촌동": "Seokchon-dong, Songpa-gu, Seoul",
    "송파동": "Songpa-dong, Songpa-gu, Seoul",
    "가락동": "Garak-dong, Songpa-gu, Seoul",
    "문정동": "Munjeong-dong, Songpa-gu, Seoul",
    
    # 강동구
    "천호동": "Cheonho-dong, Gangdong-gu, Seoul",
    "강일동": "Gangil-dong, Gangdong-gu, Seoul",
    "둔촌동": "Dunchon-dong, Gangdong-gu, Seoul",
    
    # 마포구
    "홍대": "Hongdae, Mapo-gu, Seoul",
    "상수동": "Sangsu-dong, Mapo-gu, Seoul",
    "합정동": "Hapjeong-dong, Mapo-gu, Seoul",
    "망원동": "Mangwon-dong, Mapo-gu, Seoul",
    "연남동": "Yeonnam-dong, Mapo-gu, Seoul",
    "성산동": "Seongsan-dong, Mapo-gu, Seoul",
    
    # 용산구
    "이태원": "Itaewon, Yongsan-gu, Seoul",
    "한남동": "Hannam-dong, Yongsan-gu, Seoul",
    "용산동": "Yongsan-dong, Yongsan-gu, Seoul",
    "서빙고동": "Seobinggo-dong, Yongsan-gu, Seoul",
    
    # 종로구
    "종로": "Jongno, Jongno-gu, Seoul",
    "인사동": "Insadong, Jongno-gu, Seoul",
    "삼청동": "Samcheong-dong, Jongno-gu, Seoul",
    "북촌": "Bukchon, Jongno-gu, Seoul",
    "명동": "Myeongdong, Jung-gu, Seoul",
    
    # 성동구
    "성수동": "Seongsu-dong, Seongdong-gu, Seoul",
    "왕십리": "Wangsimni, Seongdong-gu, Seoul",
    
    # 광진구
    "건대": "Konkuk University, Gwangjin-gu, Seoul",
    "자양동": "Jayang-dong, Gwangjin-gu, Seoul",
}

def get_all_korean_locations():
    """모든 한국 지역 데이터를 합친 딕셔너리를 반환합니다."""
    all_locations = {}
    all_locations.update(KOREA_REGIONS)
    all_locations.update(SEOUL_DISTRICTS)
    all_locations.update(BUSAN_DISTRICTS)
    all_locations.update(INCHEON_DISTRICTS)
    all_locations.update(SEOUL_DONG_AREAS)
    return all_locations

def search_korean_location(query):
    """
    한글 검색어로 영문 지역명을 찾습니다.
    부분 검색을 지원합니다.
    """
    all_locations = get_all_korean_locations()
    
    # 정확한 매치 우선
    if query in all_locations:
        return all_locations[query]
    
    # 부분 매치 검색
    matches = []
    for korean_name, english_name in all_locations.items():
        if query in korean_name:
            matches.append((korean_name, english_name))
    
    # 가장 짧은 매치를 우선으로 반환 (더 정확한 매치)
    if matches:
        matches.sort(key=lambda x: len(x[0]))
        return matches[0][1]
    
    return None

def get_popular_korean_locations():
    """인기 한국 지역 목록을 반환합니다."""
    return [
        "서울", "강남구", "홍대", "명동", "잠실동",
        "부산", "해운대구", "대구", "인천", "광주",
        "대전", "울산", "수원", "성남", "고양",
        "용인", "부천", "안산", "춘천", "제주"
    ]