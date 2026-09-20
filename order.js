const content = document.getElementById("content");
const progress = document.getElementById("progress");

let currentPage = 1;
const totalPages = 10;

let selectedFeeling = "";

/* =========================
   الصور
========================= */

const images = {
    background: "../images/background.png",
    book: "../images/book.png",
    desk: "../images/desk.png",
    happy: "../images/happy.png",
    pin: "../images/pin.png",
    put: "../images/put.png",
    putting: "../images/putting.png",
    stand: "../images/stand.png",
    stuff: "../images/stuff.png",
    water: "../images/water.png",
    clean: "../images/clean.png"
};

/* =========================
   التنقل
========================= */

function updateProgress() {
    progress.textContent = `${currentPage} / ${totalPages}`;
}

function nextPage() {
    if (currentPage < totalPages) {
        currentPage++;
        renderPage();
    }
}

function goBack() {
    if (currentPage > 1) {
        currentPage--;
        renderPage();
    } else {
        window.location.href = "challenges.html";
    }
}

function renderPage() {

    updateProgress();

    switch (currentPage) {
        case 1:
            page1();
            break;

        case 2:
            page2();
            break;

        case 3:
            page3();
            break;

        case 4:
            page4();
            break;

        case 5:
            page5();
            break;

        case 6:
            page6();
            break;

        case 7:
            page7();
            break;

        case 8:
            page8();
            break;

        case 9:
            page9();
            break;

        case 10:
            page10();
            break;
    }
}


/* =========================
   الصفحة 1
========================= */

function page1() {

    content.className = "page-card scene-card order-intro";

    content.innerHTML = `
        <img
            src="${images.background}"
            class="background-page"
            alt=""
        >

        <div class="background-overlay intro-layout">

            <div class="scene-text">
                <h1>ترتيبي يتغيّر</h1>

                <p>
                    أحيانًا نرتب أغراضنا بطريقة نحبها،
                    لكن يمكننا تجربة ترتيب جديد بأمان 💛
                </p>
            </div>

            <button
                class="main-btn"
                onclick="nextPage()"
            >
                لنبدأ
            </button>

        </div>
    `;
}


/* =========================
   الصفحة 2
========================= */

function page2() {

    content.className = "page-card scene-card";

    content.innerHTML = `
        <img
            src="${images.background}"
            class="background-page"
            alt=""
        >

        <div class="background-overlay">

          
        <div class="scene-text top-text"
     style="
       position:absolute;
       top:70px;
       right:40px;
       left:auto;
       width:50%;
       max-width:520px;
       transform:none;
       z-index:10;
     ">
                <h2>أجهّز حقيبتي</h2>

                <p>
                    عادةً أحب أن أضع أغراضي
                    بترتيب أعرفه.
                </p>
            </div>

          
            <button
    class="main-btn"
    onclick="nextPage()"
    style="
        position:absolute;
        top:480px;
        right:calc(40px + 25% - 110px);
        width:220px;
        z-index:20;
    "
>
    التالي
</button>

        </div>
    `;
}


/* =========================
   الصفحة 3
========================= */

function page3() {

    content.className = "page-card scene-card";

    content.innerHTML = `
        <img
            src="${images.desk}"
            class="background-page"
            alt=""
        >

        <div class="background-overlay">

            <div class="scene-text top-text">
                <h2>هذا ترتيبي المعتاد</h2>

                <p>
                    أعرف كيف أرتب أغراضي كل يوم.
                </p>
            </div>

            <div class="items-row">

                <div class="item-box">
                    <img src="${images.book}">
                    <span>الدفتر</span>
                </div>

                <div class="item-box">
                    <img src="${images.pin}">
                    <span>القلم</span>
                </div>

                <div class="item-box">
                    <img src="${images.water}">
                    <span>الماء</span>
                </div>

                <div class="item-box">
                    <img src="${images.clean}">
                    <span>المنديل</span>
                </div>

            </div>

            <button
                class="main-btn"
                onclick="nextPage()"
            >
                التالي
            </button>

        </div>
    `;
}


/* =========================
   الصفحة 4
========================= */

function page4() {

    content.className = "page-card scene-card";

    content.innerHTML = `
        <img
            src="${images.desk}"
            class="background-page"
            alt=""
        >

        <div class="background-overlay">

            <div class="scene-text top-text">
                <h2>اليوم سنجرّب تغييرًا صغيرًا!</h2>

                <p>
                    سنضع الأشياء بترتيب مختلف.
                    أغراضي نفسها، فقط الترتيب سيتغيّر 💛
                </p>
            </div>

            <img
                src="${images.put}"
                class="character-image"
                alt="الطفل والحقيبة"
            >

            <button
                class="main-btn"
                onclick="nextPage()"
            >
                أنا مستعد
            </button>

        </div>
    `;
}


/* =========================
   الصفحة 5 - التحدي
========================= */

function page5() {

    content.className = "page-card challenge-page";

    content.innerHTML = `

        <img
            src="${images.desk}"
            class="background-page"
            alt=""
        >

        <div class="background-overlay">

            <div class="scene-text top-text">
                <h2>لنجرّب ترتيبًا جديدًا</h2>

                <p>
                    اسحب الأشياء إلى الحقيبة
                    بهذا الترتيب:
                </p>

                <strong>
                    الماء ← الدفتر ← المنديل ← القلم
                </strong>
            </div>


            <div class="packing-area">

                <img
                    src="${images.put}"
                    class="packing-child"
                    alt=""
                >

                <div
                    id="bagDrop"
                    class="bag-drop"
                >
                    ضع الأشياء هنا
                </div>

                <div class="draggable-items">

                    <img
                        src="${images.water}"
                        class="drag-item"
                        draggable="true"
                        data-item="water"
                    >

                    <img
                        src="${images.book}"
                        class="drag-item"
                        draggable="true"
                        data-item="book"
                    >

                    <img
                        src="${images.clean}"
                        class="drag-item"
                        draggable="true"
                        data-item="tissue"
                    >

                    <img
                        src="${images.pin}"
                        class="drag-item"
                        draggable="true"
                        data-item="pin"
                    >

                </div>

            </div>

        </div>
    `;

    setupDragGame();
}


/* =========================
   لعبة السحب
========================= */

let expectedOrder = [
    "water",
    "book",
    "tissue",
    "pin"
];

let currentOrderIndex = 0;


function setupDragGame() {

    currentOrderIndex = 0;

    const items =
        document.querySelectorAll(".drag-item");

    const bag =
        document.getElementById("bagDrop");


    items.forEach(item => {

        item.addEventListener(
            "dragstart",
            function(event) {

                event.dataTransfer.setData(
                    "text/plain",
                    this.dataset.item
                );
            }
        );

    });


    bag.addEventListener(
        "dragover",
        function(event) {

            event.preventDefault();
        }
    );


    bag.addEventListener(
        "drop",
        function(event) {

            event.preventDefault();

            const itemName =
                event.dataTransfer.getData("text/plain");

            checkItem(itemName);
        }
    );
}


function checkItem(itemName) {

    if (
        itemName ===
        expectedOrder[currentOrderIndex]
    ) {

        const item =
            document.querySelector(
                `[data-item="${itemName}"]`
            );

        if (item) {
            item.style.visibility = "hidden";
        }

        currentOrderIndex++;


        if (
            currentOrderIndex ===
            expectedOrder.length
        ) {

            setTimeout(() => {

                currentPage = 6;
                renderPage();

            }, 500);

        }

    } else {

        const bag =
            document.getElementById("bagDrop");

        bag.classList.add("gentle-shake");

        setTimeout(() => {
            bag.classList.remove("gentle-shake");
        }, 400);
    }
}


/* =========================
   الصفحة 6
========================= */

function page6() {

    content.className = "page-card scene-card";

    content.innerHTML = `
        <img
            src="${images.desk}"
            class="background-page"
            alt=""
        >

        <div class="background-overlay">

            <div class="scene-text top-text">
                <h2>أحسنت!</h2>

                <p>
                    وضعت أغراضك بترتيب جديد 🌟
                </p>
            </div>

            <img
                src="${images.stuff}"
                class="filled-bag"
                alt="الحقيبة بعد ترتيبها"
            >

            <button
                class="main-btn"
                onclick="nextPage()"
            >
                التالي
            </button>

        </div>
    `;
}


/* =========================
   الصفحة 7
========================= */

function page7() {

    content.className = "page-card scene-card";

    content.innerHTML = `
        <img
            src="${images.desk}"
            class="background-page"
            alt=""
        >

        <div class="background-overlay">

            <div class="scene-text">
                <h2>لقد فعلتها!</h2>

                <p>
                    تغيّر الترتيب،
                    لكن كل شيء ما زال بخير 💛
                </p>
            </div>

            <img
                src="${images.happy}"
                class="happy-child"
                alt="الطفل سعيد"
            >

            <button
                class="main-btn"
                onclick="nextPage()"
            >
                التالي
            </button>

        </div>
    `;
}


/* =========================
   الصفحة 8
========================= */

function page8() {

    content.className = "page-card";

    content.innerHTML = `

        <div class="normal-page">

            <h2>كيف كان شعورك؟</h2>

            <p>
                اختر الشعور الأقرب لك
            </p>

            <div class="feeling-grid">

                <button onclick="chooseFeeling('happy')">
                    😊
                    <span>سعيد</span>
                </button>

                <button onclick="chooseFeeling('easy')">
                    ⭐
                    <span>كان سهلًا</span>
                </button>

                <button onclick="chooseFeeling('different')">
                    🤔
                    <span>كان مختلفًا</span>
                </button>

                <button onclick="chooseFeeling('hard')">
                    💛
                    <span>كان صعبًا</span>
                </button>

            </div>

        </div>
    `;
}


function chooseFeeling(feeling) {

    selectedFeeling = feeling;

    nextPage();
}


/* =========================
   الصفحة 9
========================= */

function page9() {

    content.className = "page-card";

    content.innerHTML = `

        <div class="normal-page lesson-page">

            <h2>ماذا تعلمنا؟</h2>

            <div class="lesson-card">
                🌟 أستطيع تجربة ترتيب جديد
            </div>

            <div class="lesson-card">
                💛 التغيير لا يعني أن شيئًا سيئًا سيحدث
            </div>

            <div class="lesson-card">
                🎒 يمكنني ترتيب أغراضي بأكثر من طريقة
            </div>

            <div class="lesson-card">
                🌈 أستطيع التكيّف مع التغيير
            </div>

            <button
                class="main-btn"
                onclick="nextPage()"
            >
                التالي
            </button>

        </div>
    `;
}


/* =========================
   الصفحة 10
========================= */

function page10() {

    content.className = "page-card celebration-page";

    content.innerHTML = `

        <div class="normal-page">

            <img
                src="${images.happy}"
                class="final-child"
                alt=""
            >

            <h1>أحسنت! 🎉</h1>

            <p>
                جرّبت ترتيبًا جديدًا
                ونجحت في التغيير.
            </p>

            <h3>
                💛 أنا أستطيع تجربة أشياء جديدة
            </h3>

            <div class="final-buttons">

                <button
                    class="main-btn"
                    onclick="restartGame()"
                >
                    ألعب مرة أخرى
                </button>

                <button
                    class="secondary-btn"
                    onclick="window.location.href='challenges.html'"
                >
                    العودة إلى التحديات
                </button>

            </div>

        </div>
    `;
}


function restartGame() {

    currentPage = 1;
    selectedFeeling = "";

    renderPage();
}


/* تشغيل أول صفحة */

renderPage();