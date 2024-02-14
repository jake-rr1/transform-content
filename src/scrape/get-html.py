from selenium import webdriver
from browsermobproxy import Server
import environment
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.service import Service
import time
import requests
import httpx

# INPUTS
user = 'qinhan111'

# -----------------CODE-----------------
options = webdriver.ChromeOptions()
service = Service(executable_path='C:\\Users\\jacob\\OneDrive\\Desktop\\sidehustles\\transform-content\\src\\upload\\chromedriver.exe')
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")
options.add_argument("user-data-dir=C:\\Users\\jacob\\AppData\\Local\\Google\\Chrome Beta\\User Data\\Profile 2")
options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"

# Create a new instance of the Firefox driver
driver = webdriver.Chrome(options=options)


accountLink = f'https://www.tiktok.com/@{user}'

# Go to the Google home page
driver.get(accountLink)

time.sleep(15)

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        if '/post/item_list/?WebIdLastTim' in request.url:
            requestURL = request.url
            # print('-------------------------------------------------------------')
            # print(request.url)
            # print('-------------------------------------------------------------')
            # print(request.response.status_code)
            # print('-------------------------------------------------------------')
            # print(request.response.headers['Content-Type'])
        
client = httpx.Client(http2=True)

cookies = {
    '_ttp': '2axKzn7sexefhiVO1bvhc6TBCqv',
    'ttwid': '1%7CyzWuVYKPDEtf14Q39i5oF6mTZQI3PtnGrF7CmfWtUbU%7C1707879689%7C0974fce463654286dd14a0dd17ea79ff08157f28b0dcca1696475a5b579a480e',
    'tt_csrf_token': 'PkySxrWq-UA9ZsCYudwPGQuK-fhKRPQt-g1Y',
    'tt_chain_token': 'BZ0GG66YlcCz1xqH6//qsA==',
    'ak_bmsc': 'AC06D3F01879D795BF3369B227460E42~000000000000000000000000000000~YAAQ1MbfF9ByoYWNAQAAqOyPpRbcVriBIyrnlmmzH6jyQ1SPTNazjTrzIAJlY8diRPNXyFpqABuo6jAIhtuNXv/jGauOTzV1Dk+qTGVQF2qUZPj+i0cHLoqaXfTgyqgWoDwxQNu/giEUEfpgY7zquUMkjkwcqBGt9dh+xPYNHiO2oxVzt4EMgsw/jPWTPJtSppq83h2WC+G5ZkYdoM70q0PeW7fWKmPDX2dM1NqawRyA6HOduiki0A80Owr6CCqnrBmVbDZceDxVhO2xSLRBS9UTzmfv30agFV4TI5iJqtVJB18d8NQjkUHh4R/w0UHlCHRxe0iZWyoE1WoUMhyi2mPKRLsFOnNO7S7LnqSd9T4F646qHDo2pA5Ub5BpJznfNWzyURUpcngD',
    'tiktok_webapp_theme': 'light',
    'passport_csrf_token': '09af1b9ad079c8d6685100f123d066c2',
    'passport_csrf_token_default': '09af1b9ad079c8d6685100f123d066c2',
    'perf_feed_cache': '{%%22expireTimestamp%22:1708052400000%2C%%22itemIds%22:[%%227306252753158950187%%22%2C%%227330385314692746538%22]}',
    's_v_web_id': 'verify_lsl7hebc_BAAihxCX_igpp_4BOx_AWes_0mIY7zV1Gnfk',
    'multi_sids': '7335163384767464491%3Af4684f69a0d4f0cdfbcde1ad9b683630',
    'cmpl_token': 'AgQQAPNSF-RO0rX1Upumtp0S_621wpEO_6zZYNHO4Q',
    'sid_guard': 'f4684f69a0d4f0cdfbcde1ad9b683630%7C1707879717%7C15552000%7CMon%2C+12-Aug-2024+03%3A01%3A57+GMT',
    'uid_tt': '1edb3cfacc19380501249bbdfdf2554aa6af72718406e4d122d26e714cea497b',
    'uid_tt_ss': '1edb3cfacc19380501249bbdfdf2554aa6af72718406e4d122d26e714cea497b',
    'sid_tt': 'f4684f69a0d4f0cdfbcde1ad9b683630',
    'sessionid': 'f4684f69a0d4f0cdfbcde1ad9b683630',
    'sessionid_ss': 'f4684f69a0d4f0cdfbcde1ad9b683630',
    'sid_ucp_v1': '1.0.0-KDNjMzc4ZDUzMDMxZjkzNmE4YmZkNDNhZWE3Y2NiNTY5MDc2NjYwNGUKIAiriJH0wofv5WUQpdqwrgYYswsgDDDE-K6uBjgEQOoHEAQaB3VzZWFzdDUiIGY0Njg0ZjY5YTBkNGYwY2RmYmNkZTFhZDliNjgzNjMw',
    'ssid_ucp_v1': '1.0.0-KDNjMzc4ZDUzMDMxZjkzNmE4YmZkNDNhZWE3Y2NiNTY5MDc2NjYwNGUKIAiriJH0wofv5WUQpdqwrgYYswsgDDDE-K6uBjgEQOoHEAQaB3VzZWFzdDUiIGY0Njg0ZjY5YTBkNGYwY2RmYmNkZTFhZDliNjgzNjMw',
    'store-idc': 'useast5',
    'store-country-code': 'us',
    'store-country-code-src': 'uid',
    'tt-target-idc': 'useast5',
    'tt-target-idc-sign': '3jwG95AIkor8wM8lOUnpCeJw-OpBMbup7utj5mLEuESeHb_QKdx4uQLZLeY2qpo8tEQbDux51zmGx2Zw5Nj4JiXHJFqrhb9e0v0pfh2aIXSW4NtnmQu6iDMAM3jc_hIoQGZ-9TJVRdPY_GFY83uHMDLPXtRXa9ppmlbicQCV7BsL2PLaTn5seI9vbL7LD8jAtJWxXkkxX7NN65LzixvjVIaMmraJT4J_S7NrtEvk2IQKlDj9-AonObmv4dR8v2tjxuTODBiOsmu22CvbABh3yxzjkGvMuD-_qaQ-bs7yOGGort17WYlOrMY51nmp-yNSRkvGPHKDO6pCYxYM31jOIpD4rgo1_o_Fy93yrbcM-CaIo-uTL_I7wW15f7jn8WYadly9cCnE2ghI-53KP-fv4Er19CuH5x7CqRu4YAl_fC2m9cfxVIhlg5tMXOCZgh_Bq2tSphmF2miDYwrdnMI78_c8nzjUbZnGYVWtw3Nl4NmHLVdA2NyAeT3ZjwEM8tTe',
    'last_login_method': 'handle',
    'csrf_session_id': '886450cdf35c51eafd12ed3c94d022e4',
    'passport_fe_beating_status': 'true',
    'csrfToken': '8hUv0N0p-LVxlZM97zqwnwreJmvLJoZxBExM',
    '_waftokenid': 'eyJ2Ijp7ImEiOiJqdmJaWDlhcElIQXZ6TzVuUUJvbURuS0x0eC9xRVUyQnFtNlk1STM1Um9vPSIsImIiOjE3MDc4ODU0MDYsImMiOiJKYW4zWTVPK1ZzWmtzbG5zMWptY0gvRFkwc1YxUnEwNE5uSXpYTGo3eTRvPSJ9LCJzIjoiUzR3UjdsUHFyNnU4NUNHdFl0TENjbUZkZER2bEc2STBTNmpUcGtvSzcrUT0ifQ',
    'msToken': '8t6a90kzrA2WX6SiCRzyQFQI-0m77gkfMUFmjt5l8lvWf_0Oed8aBhs_MaE2mXLKNEorhAIKsh23oJ27BsgC6DlM6ly5Y6cZ9ryW6ey_IYzEd_8J7H4ydaL3iXdJUFKDC_UN',
    'msToken': '25vobIXWTdpcmdziyMNUyErLfvmp_nBys3iXL04sacO0yvq1uesbG_OCbigEWwbnE194sLwaeuOhN55aAYSuSzVYmcuz3iUtHLF1VEp5W65OxsfOrxvU_K7hUOmLxs70Q-hEfVr2CzaXB0k=',
    'bm_sv': '7FD4E3A4B86FBB328BB09600FF6FEB8E~YAAQyA17XI8i4KONAQAAoX3npRYQBMmHHxVncgoTKAALm03IE7yn5R16AAt6AX368FDkfYnlV+l/VwN2DoH7r6Xw5fJ8Q25JDiVjKeCjhwt8nn47L58tsYT32OgTyqZUNspD6J4Bv/hm81P9HFt2Qno/ohW4wV7J5RQCDsJCvvd6g1jTfMDVSO89N16M0oiqE9AP30JXBHT9+vFTriLJVuVgigg27tZuxArrfddwufaowheAJazW2vA7reKIiwyE~1',
    'odin_tt': 'd9a019176b30a0e32489bf245f4dabf5e34efe3e3be8dd956f2a5c9142a1bec0688a1afc7d04b5141c8f09f16d8660bc5142a2464d3a820fa0945a20587f2bc161351a8dbafbbea645068b37f6f343a8',
}

headers = {
    'authority': 'www.tiktok.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_ttp=2axKzn7sexefhiVO1bvhc6TBCqv; ttwid=1%7CyzWuVYKPDEtf14Q39i5oF6mTZQI3PtnGrF7CmfWtUbU%7C1707879689%7C0974fce463654286dd14a0dd17ea79ff08157f28b0dcca1696475a5b579a480e; tt_csrf_token=PkySxrWq-UA9ZsCYudwPGQuK-fhKRPQt-g1Y; tt_chain_token=BZ0GG66YlcCz1xqH6//qsA==; ak_bmsc=AC06D3F01879D795BF3369B227460E42~000000000000000000000000000000~YAAQ1MbfF9ByoYWNAQAAqOyPpRbcVriBIyrnlmmzH6jyQ1SPTNazjTrzIAJlY8diRPNXyFpqABuo6jAIhtuNXv/jGauOTzV1Dk+qTGVQF2qUZPj+i0cHLoqaXfTgyqgWoDwxQNu/giEUEfpgY7zquUMkjkwcqBGt9dh+xPYNHiO2oxVzt4EMgsw/jPWTPJtSppq83h2WC+G5ZkYdoM70q0PeW7fWKmPDX2dM1NqawRyA6HOduiki0A80Owr6CCqnrBmVbDZceDxVhO2xSLRBS9UTzmfv30agFV4TI5iJqtVJB18d8NQjkUHh4R/w0UHlCHRxe0iZWyoE1WoUMhyi2mPKRLsFOnNO7S7LnqSd9T4F646qHDo2pA5Ub5BpJznfNWzyURUpcngD; tiktok_webapp_theme=light; passport_csrf_token=09af1b9ad079c8d6685100f123d066c2; passport_csrf_token_default=09af1b9ad079c8d6685100f123d066c2; perf_feed_cache={%22expireTimestamp%22:1708052400000%2C%22itemIds%22:[%227306252753158950187%22%2C%227330385314692746538%22]}; s_v_web_id=verify_lsl7hebc_BAAihxCX_igpp_4BOx_AWes_0mIY7zV1Gnfk; multi_sids=7335163384767464491%3Af4684f69a0d4f0cdfbcde1ad9b683630; cmpl_token=AgQQAPNSF-RO0rX1Upumtp0S_621wpEO_6zZYNHO4Q; sid_guard=f4684f69a0d4f0cdfbcde1ad9b683630%7C1707879717%7C15552000%7CMon%2C+12-Aug-2024+03%3A01%3A57+GMT; uid_tt=1edb3cfacc19380501249bbdfdf2554aa6af72718406e4d122d26e714cea497b; uid_tt_ss=1edb3cfacc19380501249bbdfdf2554aa6af72718406e4d122d26e714cea497b; sid_tt=f4684f69a0d4f0cdfbcde1ad9b683630; sessionid=f4684f69a0d4f0cdfbcde1ad9b683630; sessionid_ss=f4684f69a0d4f0cdfbcde1ad9b683630; sid_ucp_v1=1.0.0-KDNjMzc4ZDUzMDMxZjkzNmE4YmZkNDNhZWE3Y2NiNTY5MDc2NjYwNGUKIAiriJH0wofv5WUQpdqwrgYYswsgDDDE-K6uBjgEQOoHEAQaB3VzZWFzdDUiIGY0Njg0ZjY5YTBkNGYwY2RmYmNkZTFhZDliNjgzNjMw; ssid_ucp_v1=1.0.0-KDNjMzc4ZDUzMDMxZjkzNmE4YmZkNDNhZWE3Y2NiNTY5MDc2NjYwNGUKIAiriJH0wofv5WUQpdqwrgYYswsgDDDE-K6uBjgEQOoHEAQaB3VzZWFzdDUiIGY0Njg0ZjY5YTBkNGYwY2RmYmNkZTFhZDliNjgzNjMw; store-idc=useast5; store-country-code=us; store-country-code-src=uid; tt-target-idc=useast5; tt-target-idc-sign=3jwG95AIkor8wM8lOUnpCeJw-OpBMbup7utj5mLEuESeHb_QKdx4uQLZLeY2qpo8tEQbDux51zmGx2Zw5Nj4JiXHJFqrhb9e0v0pfh2aIXSW4NtnmQu6iDMAM3jc_hIoQGZ-9TJVRdPY_GFY83uHMDLPXtRXa9ppmlbicQCV7BsL2PLaTn5seI9vbL7LD8jAtJWxXkkxX7NN65LzixvjVIaMmraJT4J_S7NrtEvk2IQKlDj9-AonObmv4dR8v2tjxuTODBiOsmu22CvbABh3yxzjkGvMuD-_qaQ-bs7yOGGort17WYlOrMY51nmp-yNSRkvGPHKDO6pCYxYM31jOIpD4rgo1_o_Fy93yrbcM-CaIo-uTL_I7wW15f7jn8WYadly9cCnE2ghI-53KP-fv4Er19CuH5x7CqRu4YAl_fC2m9cfxVIhlg5tMXOCZgh_Bq2tSphmF2miDYwrdnMI78_c8nzjUbZnGYVWtw3Nl4NmHLVdA2NyAeT3ZjwEM8tTe; last_login_method=handle; csrf_session_id=886450cdf35c51eafd12ed3c94d022e4; passport_fe_beating_status=true; csrfToken=8hUv0N0p-LVxlZM97zqwnwreJmvLJoZxBExM; _waftokenid=eyJ2Ijp7ImEiOiJqdmJaWDlhcElIQXZ6TzVuUUJvbURuS0x0eC9xRVUyQnFtNlk1STM1Um9vPSIsImIiOjE3MDc4ODU0MDYsImMiOiJKYW4zWTVPK1ZzWmtzbG5zMWptY0gvRFkwc1YxUnEwNE5uSXpYTGo3eTRvPSJ9LCJzIjoiUzR3UjdsUHFyNnU4NUNHdFl0TENjbUZkZER2bEc2STBTNmpUcGtvSzcrUT0ifQ; msToken=8t6a90kzrA2WX6SiCRzyQFQI-0m77gkfMUFmjt5l8lvWf_0Oed8aBhs_MaE2mXLKNEorhAIKsh23oJ27BsgC6DlM6ly5Y6cZ9ryW6ey_IYzEd_8J7H4ydaL3iXdJUFKDC_UN; msToken=25vobIXWTdpcmdziyMNUyErLfvmp_nBys3iXL04sacO0yvq1uesbG_OCbigEWwbnE194sLwaeuOhN55aAYSuSzVYmcuz3iUtHLF1VEp5W65OxsfOrxvU_K7hUOmLxs70Q-hEfVr2CzaXB0k=; bm_sv=7FD4E3A4B86FBB328BB09600FF6FEB8E~YAAQyA17XI8i4KONAQAAoX3npRYQBMmHHxVncgoTKAALm03IE7yn5R16AAt6AX368FDkfYnlV+l/VwN2DoH7r6Xw5fJ8Q25JDiVjKeCjhwt8nn47L58tsYT32OgTyqZUNspD6J4Bv/hm81P9HFt2Qno/ohW4wV7J5RQCDsJCvvd6g1jTfMDVSO89N16M0oiqE9AP30JXBHT9+vFTriLJVuVgigg27tZuxArrfddwufaowheAJazW2vA7reKIiwyE~1; odin_tt=d9a019176b30a0e32489bf245f4dabf5e34efe3e3be8dd956f2a5c9142a1bec0688a1afc7d04b5141c8f09f16d8660bc5142a2464d3a820fa0945a20587f2bc161351a8dbafbbea645068b37f6f343a8',
    'referer': accountLink,
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Opera";v="106"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
}

try:
    # Perform the request
    response = client.get(requestURL, headers=headers, cookies=cookies)

    # Check if the response was received via HTTP/2
    protocol = response.http_version
    print(f'Response received via: {protocol}')

    # Print the response
    print(response.text)

finally:
    # Close the client
    client.close()