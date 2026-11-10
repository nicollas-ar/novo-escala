(() => {
  const abrir = document.getElementById("abrir-menu");
  const menu = document.getElementById("menu-lateral");

  abrir.hidden = false;
  abrir.addEventListener("click", () => {
    menu.showModal();
    abrir.setAttribute("aria-expanded", "true");
  });

  menu.addEventListener("click", (evento) => {
    if (evento.target === menu) menu.close();
  });

  menu.addEventListener("close", () => {
    abrir.setAttribute("aria-expanded", "false");
  });
})();
