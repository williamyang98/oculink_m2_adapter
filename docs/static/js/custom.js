class Popups {
  constructor() {
    this.elems = {};

    let popup_elems = document.getElementsByClassName("popup");
    for (let popup_elem of popup_elems) {
      let id = popup_elem.getAttribute("id");
      if (id !== null) {
        this.elems[id] = popup_elem;
      } else {
        continue;
      }

      popup_elem.classList.add("inactive");
      let popup_background = popup_elem.querySelector(".popup-background");
      popup_background.addEventListener("click", (ev) => {
        ev.preventDefault();
        this.close_popups();
      });
    }
  }

  close_popups() {
    for (let id in this.elems) {
      let elem = this.elems[id];
      elem.classList.add("inactive");
    }
  }

  show_popup(id) {
    let elem = this.elems[id];
    elem.classList.remove("inactive");
  }

  get_popup(id) {
    let elem = this.elems[id];
    let background = elem.querySelector(".popup-background");
    return background;
  }
}

class ResponsiveImages {
  constructor(popups) {
    let id = "popup-images";
    let popup_elem = popups.get_popup(id);
    let popup_image = popup_elem.querySelector("img");

    let images = document.getElementsByClassName("responsive-image");
    for (let image of images) {
      let elem = image.querySelector("img");
      elem.addEventListener("click", (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        popup_image.src = elem.src;
        popups.show_popup(id);
      });
    }
    this.images = images;
  }
}

export { Popups, ResponsiveImages };
