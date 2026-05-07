<template>
  <div class="policy-page">
    <div class="global-page-container">
      <div class="policy-wrapper">
        <header class="policy-header">
          <p class="policy-label">Legal</p>
          <h1 class="policy-title">개인정보처리방침</h1>
          <p class="policy-date">시행일: 2026년 4월 28일</p>
        </header>
        <div class="policy-body">
          <section class="policy-section">
            <h2>제1조 (총칙)</h2>
            <p>(주) 아띠끄디자인(이하 "회사")은 이용자의 개인정보를 소중히 여기며, 「개인정보 보호법」 및 관련 법령을 준수합니다. 본 방침은 회사가 운영하는 웹사이트(이하 "사이트")를 통해 수집하는 개인정보의 처리 목적, 보유 기간, 권리 보호 방법 등을 안내합니다.</p>
          </section>
          <section class="policy-section">
            <h2>제2조 (수집하는 개인정보 항목 및 수집 방법)</h2>
            <p>회사는 방문 상담 예약 접수를 위해 아래 항목을 수집합니다.</p>
            <table class="policy-table">
              <thead><tr><th>구분</th><th>항목</th><th>필수 여부</th></tr></thead>
              <tbody>
                <tr><td>기본 정보</td><td>이름, 연락처(전화번호), 방문 희망 일시</td><td>필수</td></tr>
                <tr><td>연락 정보</td><td>이메일 주소</td><td>선택</td></tr>
                <tr><td>상담 관련 정보</td><td>공간 형태 및 평형대, 선호 브랜드/스타일, 필요 가구 품목</td><td>선택</td></tr>
                <tr><td>시공 관련 정보</td><td>현장 주소, 공사 희망일, 전체 예산, 도면/현장 사진</td><td>선택 (인테리어·토탈 상담 시)</td></tr>
              </tbody>
            </table>
            <p class="policy-note">수집 방법: 사이트 내 방문 상담 예약 폼을 통한 이용자 직접 입력<br>※ 방문 예약을 네이버 예약 시스템을 통해 진행하시는 경우, 해당 과정에서 수집되는 개인정보는 네이버의 개인정보처리방침에 따라 처리되며, 회사는 그 내용에 대해 책임을 지지 않습니다.</p>
          </section>
          <section class="policy-section">
            <h2>제3조 (개인정보 수집 및 이용 목적)</h2>
            <ul>
              <li>방문 상담 예약 접수 및 일정 확인</li>
              <li>상담 진행을 위한 담당자 연락</li>
              <li>상담 내용에 맞는 맞춤형 서비스 제공</li>
            </ul>
          </section>
          <section class="policy-section">
            <h2>제4조 (개인정보 보유 및 이용 기간)</h2>
            <p>수집한 개인정보는 상담 완료 후 <strong>1년</strong>이 경과하면 파기합니다. 단, 이용자가 삭제를 요청할 경우 지체 없이 파기합니다.</p>
          </section>
          <section class="policy-section">
            <h2>제5조 (개인정보의 제3자 제공)</h2>
            <p>회사는 이용자의 동의 없이 개인정보를 제3자에게 제공하지 않습니다. 단, 법령에 의한 요청이 있을 경우는 예외로 합니다.</p>
          </section>
          <section class="policy-section">
            <h2>제6조 (개인정보 처리 위탁)</h2>
            <p>현재 회사는 개인정보 처리를 외부 업체에 위탁하지 않습니다. 향후 위탁 발생 시 본 방침에 해당 내용을 공개하겠습니다.</p>
          </section>
          <section class="policy-section">
            <h2>제7조 (이용자의 권리와 행사 방법)</h2>
            <ul>
              <li>개인정보 열람 요청</li>
              <li>개인정보 수정·삭제 요청</li>
              <li>개인정보 처리 정지 요청</li>
            </ul>
            <p>권리 행사는 아래 개인정보 보호책임자에게 이메일 또는 전화로 연락 주시면 지체 없이 조치합니다.</p>
          </section>
          <section class="policy-section">
            <h2>제8조 (개인정보 보호책임자)</h2>
            <table class="policy-table">
              <tbody>
                <tr><td>성명</td><td>홍민영</td></tr>
                <tr><td>직책</td><td>대표이사</td></tr>
                <tr><td>이메일</td><td>attique_@naver.com</td></tr>
                <tr><td>전화</td><td>02-3443-8170</td></tr>
              </tbody>
            </table>
          </section>
          <section class="policy-section">
            <h2>제9조 (개인정보처리방침 변경)</h2>
            <p>본 방침은 법령 또는 서비스 변경에 따라 개정될 수 있습니다. 변경 시 사이트 공지사항을 통해 사전에 안내합니다.</p>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.policy-page { background-color: #F5F0E8; min-height: calc(100vh - 160px); }
.policy-wrapper { max-width: 800px; margin: 0 auto; padding: 5rem 1.5rem 6rem; }
.policy-header { margin-bottom: 3.5rem; border-bottom: 1px solid rgba(149,55,53,0.2); padding-bottom: 2rem; }
.policy-label { font-family: 'Montserrat', sans-serif; font-size: 10px; text-transform: uppercase; letter-spacing: 0.25em; color: #953735; margin: 0 0 0.75rem; }
.policy-title { font-family: 'Pretendard', sans-serif; font-size: 1.75rem; font-weight: 500; color: #2c2c2c; margin: 0 0 0.75rem; }
.policy-date { font-family: 'Pretendard', sans-serif; font-size: 12px; color: #888; margin: 0; }
.policy-body { display: flex; flex-direction: column; gap: 2.5rem; }
.policy-section h2 { font-family: 'Pretendard', sans-serif; font-size: 14px; font-weight: 600; color: #953735; margin: 0 0 1rem; letter-spacing: 0.02em; }
.policy-section p, .policy-section li { font-family: 'Pretendard', sans-serif; font-size: 13px; line-height: 2; color: #444; margin: 0 0 0.5rem; }
.policy-section ul { padding-left: 1.2rem; margin: 0.5rem 0; }
.policy-section li { margin: 0; }
.policy-note { font-size: 12px !important; color: #777 !important; background: rgba(149,55,53,0.05); padding: 0.8rem 1rem; border-left: 2px solid rgba(149,55,53,0.3); margin-top: 0.75rem !important; line-height: 1.8 !important; }
.policy-table { width: 100%; border-collapse: collapse; margin: 0.75rem 0; font-family: 'Pretendard', sans-serif; font-size: 12px; }
.policy-table th, .policy-table td { border: 1px solid rgba(149,55,53,0.15); padding: 0.6rem 0.9rem; text-align: left; line-height: 1.6; color: #444; }
.policy-table th { background: rgba(149,55,53,0.08); font-weight: 600; color: #2c2c2c; }
.policy-table td:first-child { white-space: nowrap; font-weight: 500; color: #333; }
@media (max-width: 768px) {
  .policy-wrapper { padding: 3rem 1.25rem 4rem; }
  .policy-title { font-size: 1.4rem; }
  .policy-table { font-size: 11px; }
  .policy-table th, .policy-table td { padding: 0.5rem 0.6rem; }
}
</style>
