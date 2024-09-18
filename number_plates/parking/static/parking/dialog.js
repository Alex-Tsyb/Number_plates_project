function init_widgets_for_htmx_element(target) {

    const main_window = document.querySelector('body');
    // init other widgets

    // init modal dialogs
    if (target.tagName === 'DIALOG') {
        target.showModal();
        main_window.style.overflowY = 'hidden';
        htmx.on('.close-dialog', 'click', function(event) {
            var dialog = htmx.find('dialog[open]');
            dialog.close();
            main_window.style.overflowY = 'auto';
            htmx.remove(dialog);
        });
    }
}

htmx.onLoad(init_widgets_for_htmx_element);