import { MDCDrawer } from "@material/drawer/index";
import { MDCList } from '@material/list/index';
import { MDCMenu } from '@material/menu/index';
import { MDCRipple } from '@material/ripple/index';
import { MDCTextField } from '@material/textfield/index';
import { MDCTopAppBar } from '@material/top-app-bar/index';


// Component instantiation

//const drawer = MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));

const lists = [].map.call(document.querySelectorAll('.mdc-list'), (el) => {
  return new MDCList(el);
});

const menu = new MDCMenu(document.querySelector('.mdc-menu'));

const ripples = [].map.call(document.querySelectorAll('.mdc-button, .mdc-list'), (el) => {
  return new MDCRipple(el);
});

const textFields = [].map.call(document.querySelectorAll('.mdc-text-field'), (el) => {
  return new MDCTextField(el);
});

const topAppBar = new MDCTopAppBar(document.querySelector('.mdc-top-app-bar'));


// Drawer (modal) functionality

// Highlight active link
const activeLink = document.querySelector('.mdc-drawer .mdc-list-item[href=\"' + document.location.pathname.toString() + '\"]');
const precedentLink = document.getElementById('precedent-link');
if (activeLink) {
  activeLink.classList.add('mdc-list-item--activated');
  activeLink.setAttribute('aria-current', 'page');
} else {
  precedentLink.insertAdjacentHTML('afterend', '<a class=\"mdc-list-item mdc-list-item--activated\" href=\"' + document.location.pathname.toString() + '\" aria-current=\"page\"><span class="mdc-list-item__text">' + document.title.substring(8) + '<\/span><\/a>');
}
const drawer = MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));

// Toggle drawer on navigation button click
//const topAppBar = MDCTopAppBar.attachTo(document.getElementById('app-bar'));
topAppBar.setScrollTarget(document.getElementById('main-content'));
topAppBar.listen('MDCTopAppBar:nav', () => {
  drawer.open = !drawer.open;
});

// Close drawer when item activated
document.querySelector('.mdc-drawer .mdc-list').addEventListener('click', () => {
  drawer.open = false;
});

// Focus on first focusable element after drawer closed
document.body.addEventListener('MDCDrawer:closed', () => {
  document.getElementById('main-content').querySelector(
    "a[href]:not([tabindex='-1']),"
    + "area[href]:not([tabindex='-1']),"
    + "input:not([disabled]):not([tabindex='-1']),"
    + "select:not([disabled]):not([tabindex='-1']),"
    + "textarea:not([disabled]):not([tabindex='-1']),"
    + "button:not([disabled]):not([tabindex='-1']),"
    + "iframe:not([tabindex='-1']),"
    + "[tabindex]:not([tabindex='-1']),"
    + "[contentEditable=true]:not([tabindex='-1'])"
  ).focus();
  //document.getElementById('main-content').querySelector('input, button').focus();
});


// Menu functionality

// Close menu on load
menu.open = false;

// Open menu on menu button click
document.getElementById('menu-button').addEventListener('click', () => {
  menu.open = true;
});
