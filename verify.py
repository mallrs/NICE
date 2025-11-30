import asyncio
import os  # os 모듈 추가
from verification import Verification

async def main():
    # 사용자로부터 입력 받기
    name = input("이름을 입력해주세요: ")
    birthdate = input("생년월일을 입력해주세요 (예: YYMMDDX): ")
    phone = input("전화번호를 입력해주세요: ")
    ISP = input("통신사를 입력해주세요 (예: SK, KT, LG (알뜰폰 SM, KM, LM): ")
    
    try:
        verification = Verification(ISP)

    except:
        return {"Success": False, "Message": "올바른 ISP 값을 입력해주세요."}
    
    initResult = await verification.initSession()
    if not initResult['Success']:
        return {"Success": False, "Message": initResult['Message']}

    captchaResult = await verification.getCaptcha()
    try:
        # 캡챠 이미지를 지정된 경로에 저장
        captcha_path = 'C:\\Users\\USER\\Desktop\\NICE 인증기\\captcha.png'
        with open(captcha_path, 'wb') as f:
            f.write(captchaResult)
    
    except:
        return {"Success": False, "Message": "캡챠 이미지를 저장하던 중 오류가 발생하였습니다."}

    # 캡챠 이미지 자동 열기
    os.startfile(captcha_path)  # Windows에서 파일 열기

    captchaCode = input("캡챠 코드를 입력해주세요: ")
    sendResult = await verification.sendSmsCode(name, birthdate, phone, captchaCode)
    if not sendResult['Success']:
        return {"Success": False, "Message": sendResult['Message']}
    
    smsCode = input("SMS로 전송된 코드를 입력해주세요: ")
    checkResult = await verification.checkSmsCode(smsCode)
    if not checkResult['Success']:
        return {"Success": False, "Message": checkResult['Message']}

    print("인증이 성공적으로 완료되었어요!")
    return {"Success": True, "Message": "인증이 성공적으로 완료되었습니다."}

asyncio.run(main())
