/* ============================================
   PAGE TRANSITION — Fade In/Out
   Setiap klik link internal → halaman fade out
   Halaman baru → fade in
   ============================================ */

(function () {

    // ============================================
    // FADE IN SAAT HALAMAN BARU DIMUAT
    // ============================================
    function fadeInPage() {
        // Set opacity ke 0 dulu (kalau belum)
        document.body.classList.remove('page-exit');
        // Delay sedikit biar CSS transition trigger
        requestAnimationFrame(() => {
            document.body.classList.add('page-loaded');
        });
    }

    // ============================================
    // INTERCEPT KLIK LINK INTERNAL
    // ============================================
    function setupLinkInterception() {
        document.querySelectorAll('a').forEach(link => {
            const href = link.getAttribute('href');

            // Skip kalau:
            // - tidak ada href
            // - link eksternal (http/https yang bukan domain sendiri)
            // - anchor (#)
            // - mailto / tel / wa.me
            // - target="_blank"
            if (
                !href ||
                href.startsWith('http') ||
                href.startsWith('#') ||
                href.startsWith('mailto:') ||
                href.startsWith('tel:') ||
                href.startsWith('wa.me') ||
                link.getAttribute('target') === '_blank'
            ) {
                return;
            }

            link.addEventListener('click', (e) => {
                // Skip kalau user pakai Ctrl/Cmd/Shift + klik
                if (e.ctrlKey || e.metaKey || e.shiftKey) return;

                e.preventDefault();

                // Fade out halaman lama
                document.body.classList.add('page-exit');
                document.body.classList.remove('page-loaded');

                // Navigasi setelah fade out selesai (350ms)
                setTimeout(() => {
                    window.location.href = href;
                }, 350);
            });
        });
    }

    // ============================================
    // HANDLE BACK/FORWARD BROWSER
    // ============================================
    window.addEventListener('pageshow', (e) => {
        // Kalau kembali dari cache (back button)
        if (e.persisted) {
            fadeInPage();
        }
    });

    // ============================================
    // START
    // ============================================
    // Tunggu DOM siap
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            fadeInPage();
            setupLinkInterception();
        });
    } else {
        fadeInPage();
        setupLinkInterception();
    }

})();