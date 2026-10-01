/* =====================================================
   CAREERAI DASHBOARD JAVASCRIPT
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {


        /* =========================================
           DASHBOARD CARD ANIMATION
        ========================================= */

        const cards =
            document.querySelectorAll(
                ".dashboard-card, .card"
            );


        cards.forEach(function (card, index) {

            card.style.opacity = "0";

            card.style.transform =
                "translateY(10px)";


            setTimeout(function () {

                card.style.opacity = "1";

                card.style.transform =
                    "translateY(0)";

                card.style.transition =
                    "opacity 0.35s ease, transform 0.35s ease";

            }, index * 50);

        });


        /* =========================================
           PROFILE COMPLETION
        ========================================= */

        const progress =
            document.querySelector(
                ".progress-fill"
            );


        if (progress) {

            const fields = [
                "education",
                "skills",
                "experience",
                "interests",
                "career_goal",
                "bio"
            ];


            let completed = 0;


            fields.forEach(function (field) {

                const element =
                    document.getElementById(field);

                if (
                    element &&
                    element.value.trim() !== ""
                ) {

                    completed++;

                }

            });


            const percentage =
                Math.round(
                    (completed / fields.length) *
                    100
                );


            progress.style.width =
                percentage + "%";


            const progressText =
                document.querySelector(
                    ".progress-text"
                );


            if (progressText) {

                progressText.textContent =
                    percentage +
                    "% Profile Complete";

            }

        }

    }
);