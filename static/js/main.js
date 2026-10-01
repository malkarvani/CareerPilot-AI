/* =====================================================
   CAREERAI MAIN JAVASCRIPT
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {


        /* =====================================
           SIDEBAR
        ===================================== */

        const sidebar =
            document.getElementById(
                "sidebar"
            );


        const mobileMenu =
            document.getElementById(
                "mobileMenu"
            );


        const sidebarClose =
            document.getElementById(
                "sidebarClose"
            );


        const overlay =
            document.getElementById(
                "sidebarOverlay"
            );


        function openSidebar() {

            if (!sidebar) return;

            sidebar.classList.add(
                "open"
            );

            if (overlay) {

                overlay.classList.add(
                    "show"
                );

            }

        }


        function closeSidebar() {

            if (!sidebar) return;

            sidebar.classList.remove(
                "open"
            );

            if (overlay) {

                overlay.classList.remove(
                    "show"
                );

            }

        }


        if (mobileMenu) {

            mobileMenu.addEventListener(
                "click",
                openSidebar
            );

        }


        if (sidebarClose) {

            sidebarClose.addEventListener(
                "click",
                closeSidebar
            );

        }


        if (overlay) {

            overlay.addEventListener(
                "click",
                closeSidebar
            );

        }



        /* =====================================
           ACTIVE SIDEBAR LINK
        ===================================== */

        const currentPath =
            window.location.pathname;


        const navItems =
            document.querySelectorAll(
                ".nav-item"
            );


        navItems.forEach(
            function (item) {

                const href =
                    item.getAttribute(
                        "href"
                    );


                if (
                    href &&
                    href !== "/" &&
                    currentPath.startsWith(
                        href
                    )
                ) {

                    item.classList.add(
                        "active"
                    );

                }

            }
        );


    }
);