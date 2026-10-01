/* =========================================================
   CAREERAI FLOATING AI BUTTON
========================================================= */

(function () {

    "use strict";


    const aiButton =
        document.getElementById("floatingAI");


    if (!aiButton) {

        return;

    }



    /* =========================================
       ENTRANCE ANIMATION
    ========================================= */

    aiButton.style.opacity = "0";

    aiButton.style.transform =
        "translateY(20px)";


    setTimeout(function () {

        aiButton.style.transition =
            "opacity 0.5s ease, transform 0.5s ease";


        aiButton.style.opacity = "1";


        aiButton.style.transform =
            "translateY(0)";

    }, 500);



    /* =========================================
       CLICK ANIMATION
    ========================================= */

    aiButton.addEventListener(
        "click",
        function () {

            aiButton.classList.add(
                "ai-clicked"
            );


            setTimeout(
                function () {

                    aiButton.classList.remove(
                        "ai-clicked"
                    );

                },
                300
            );

        }
    );



    /* =========================================
       TOOLTIP
    ========================================= */

    let tooltip;


    function createTooltip() {


        tooltip =
            document.createElement(
                "div"
            );


        tooltip.textContent =
            "Ask CareerAI";


        tooltip.style.position =
            "fixed";


        tooltip.style.right =
            "25px";


        tooltip.style.bottom =
            "95px";


        tooltip.style.padding =
            "8px 12px";


        tooltip.style.borderRadius =
            "8px";


        tooltip.style.background =
            "#111827";


        tooltip.style.color =
            "#ffffff";


        tooltip.style.fontSize =
            "12px";


        tooltip.style.fontWeight =
            "600";


        tooltip.style.zIndex =
            "1300";


        tooltip.style.opacity =
            "0";


        tooltip.style.pointerEvents =
            "none";


        tooltip.style.transition =
            "opacity 0.2s ease";


        document.body.appendChild(
            tooltip
        );

    }



    createTooltip();



    /* =========================================
       HOVER
    ========================================= */

    aiButton.addEventListener(
        "mouseenter",
        function () {

            if (tooltip) {

                tooltip.style.opacity =
                    "1";

            }

        }
    );


    aiButton.addEventListener(
        "mouseleave",
        function () {

            if (tooltip) {

                tooltip.style.opacity =
                    "0";

            }

        }
    );



    /* =========================================
       KEYBOARD ACCESSIBILITY
    ========================================= */

    aiButton.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter" ||
                event.key === " "
            ) {

                event.preventDefault();

                aiButton.click();

            }

        }
    );

})();