// Sidebar functionality
function initSidebar() {
    // Toggle submenu
    document.querySelectorAll('[data-has-submenu]').forEach(item => {
        item.addEventListener('click', (e) => {
            e.stopPropagation();
            const submenuId = item.dataset.hasSubmenu;
            const submenu = document.getElementById(`${submenuId}-submenu`);

            if (submenu) {
                submenu.classList.toggle('expanded');
                item.setAttribute('data-expanded', submenu.classList.contains('expanded'));
            }
        });
    });

    // Handle navigation items
    document.querySelectorAll('.nav-item:not([data-has-submenu]), .nav-subitem').forEach(item => {
        item.addEventListener('click', () => {
            // Remove active class from all items
            document.querySelectorAll('.nav-item, .nav-subitem').forEach(i => {
                i.classList.remove('active');
            });
            item.classList.add('active');

            // Handle section change logic here
            const section = item.dataset.section;
            if (section) {
                console.log('Navigate to section:', section);
                // You can dispatch a custom event or call a function to update the main content
                window.dispatchEvent(new CustomEvent('sectionChange', { detail: { section } }));
            }
        });
    });

    // Handle logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            console.log('Logout clicked');
            // Handle logout logic here
        });
    }
}

// Call init when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSidebar);
} else {
    initSidebar();
}