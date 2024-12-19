document.addEventListener("DOMContentLoaded", function () {
    const micButton = document.getElementById("micButton");
    const userInput = document.querySelector('input[name="user_input"]');
    const chatBox = document.getElementById("chat-box");

    // 채팅창 자동 스크롤 함수
    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // 브라우저에서 음성 인식 API 확인
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.lang = "ko-KR";
        recognition.interimResults = false;

        // 마이크 버튼 클릭 이벤트
        micButton.addEventListener("click", () => {
            micButton.disabled = true;
            micButton.textContent = "듣는 중...";
            recognition.start();
        });

        // 음성 인식 결과 처리
        recognition.addEventListener("result", (event) => {
            userInput.value = event.results[0][0].transcript;
            userInput.form.submit();
            scrollToBottom();  // 채팅창 스크롤
        });

        recognition.addEventListener("speechend", () => {
            recognition.stop();
            micButton.disabled = false;
            micButton.textContent = "🎤";
        });
    } else {
        micButton.style.display = "none";
        alert("브라우저가 음성 인식을 지원하지 않습니다.");
    }

    // 채팅 페이지가 로드되면 스크롤을 최하단으로 이동
    scrollToBottom();
});
