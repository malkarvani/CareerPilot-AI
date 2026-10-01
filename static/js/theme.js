/* =========================================================
   CAREERAI THEME SYSTEM
========================================================= */

(function () {

    "use strict";


    const html =
        document.documentElement;


    const themeToggle =
        document.getElementById("themeToggle");


    const themeIcon =
        document.getElementById("themeIcon");


    const themeLabel =
        document.getElementById("themeLabel");


    const themeColor =
        document.getElementById("themeColor");



    /* =========================================
       GET CURRENT THEME
    ========================================= */

    function getTheme() {

        return html.getAttribute(
            "data-theme"
        ) || "light";

    }



    /* =========================================
       UPDATE BUTTON
    ========================================= */

    function updateThemeButton(theme) {


        if (!themeIcon) {
            return;
        }


        if (theme === "dark") {

            themeIcon.textContent = "☀️";


            if (themeLabel) {

                themeLabel.textContent =
                    "Light";

            }


            if (themeToggle) {

                themeToggle.title =
                    "Switch to Light Mode";

            }


            if (themeColor) {

                themeColor.setAttribute(
                    "content",
                    "#0b1120"
                );

            }

        }

        else {

            themeIcon.textContent = "🌙";


            if (themeLabel) {

                themeLabel.textContent =
                    "Dark";

            }


            if (themeToggle) {

                themeToggle.title =
                    "Switch to Dark Mode";

            }


            if (themeColor) {

                themeColor.setAttribute(
                    "content",
                    "#ffffff"
                );

            }

        }

    }



    /* =========================================
       SET THEME
    ========================================= */

    function setTheme(theme) {


        if (
            theme !== "dark" &&
            theme !== "light"
        ) {

            theme = "light";

        }


        html.setAttribute(
            "data-theme",
            theme
        );


        localStorage.setItem(
            "careerai-theme",
            theme
        );


        updateThemeButton(theme);

    }



    /* =========================================
       TOGGLE
    ========================================= */

    function toggleTheme() {


        const current =
            getTheme();


        const next =
            current === "dark"
                ? "light"
                : "dark";


        setTheme(next);

    }



    /* =========================================
       BUTTON CLICK
    ========================================= */

    if (themeToggle) {

        themeToggle.addEventListener(
            "click",
            toggleTheme
        );

    }



    /* =========================================
       INITIALIZE
    ========================================= */

    const savedTheme =
        localStorage.getItem(
            "careerai-theme"
        );


    if (
        savedTheme === "dark" ||
        savedTheme === "light"
    ) {

        setTheme(savedTheme);

    }

    else {

        setTheme("light");

    }



    /* =========================================
       SYSTEM THEME CHANGE
    ========================================= */

    const systemTheme =
        window.matchMedia(
            "(prefers-color-scheme: dark)"
        );


    systemTheme.addEventListener(
        "change",
        function (event) {


            const saved =
                localStorage.getItem(
                    "careerai-theme"
                );


            if (saved) {
                return;
            }


            setTheme(
                event.matches
                    ? "dark"
                    : "light"
            );

        }
    );

})();