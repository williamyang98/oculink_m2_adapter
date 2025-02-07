class Popups {
  constructor() {
    this.elems = {};

    let popup_elems = document.getElementsByClassName("popup");
    for (let popup_elem of popup_elems) {
      let id = popup_elem.getAttribute("id");
      if (id === null) continue;
      this.elems[id] = popup_elem;
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

class Carousels {
  constructor() {
    this.carousels = {};
    this.carousel_items = {}
    this.selected_carousel_indices = {};
    this.carousel_listeners = {};

    let carousels = document.getElementsByClassName("carousel");
    for (let carousel of carousels) {
      let key = carousel.getAttribute("key");
      if (key === null) continue;
      this.carousels[key] = carousel;
      this.selected_carousel_indices[key] = null;
    }

    for (let key in this.carousels) {
      let carousel = this.carousels[key];
      let items = [];
      for (let elem of carousel.children) {
        if (!elem.classList.contains("carousel-item")) continue;
        elem.classList.add("inactive");
        items.push(elem);
      }
      this.carousel_items[key] = items;
    }

    for (let key in this.carousels) {
      let carousel = this.carousels[key];
      let controls = carousel.querySelector(".carousel-controls");
      let left_button = controls.querySelector(".carousel-left");
      let right_button = controls.querySelector(".carousel-right");
      left_button.addEventListener("click", (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        let index = this.selected_carousel_indices[key];
        let total = this.carousel_items[key].length;
        let next_index = index-1;
        if (next_index < 0) next_index += total;
        this.select_carousel(key, next_index, true);
      });
      right_button.addEventListener("click", (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        let index = this.selected_carousel_indices[key];
        let total = this.carousel_items[key].length;
        let next_index = index+1;
        if (next_index >= total) next_index -= total;
        this.select_carousel(key, next_index, true);
      });
    }
    for (let key in this.carousels) {
      this.carousel_listeners[key] = new Set([]);
    }
    for (let key in this.carousels) {
      this.select_carousel(key, 0, false);
    }
  }

  select_carousel(key, index, propagate) {
    let carousel_items = this.carousel_items[key];
    let selected_carousel_index = this.selected_carousel_indices[key];
    if (selected_carousel_index !== null && selected_carousel_index !== index) {
      carousel_items[selected_carousel_index].classList.add("inactive");
    }
    if (selected_carousel_index !== index) {
      carousel_items[index].classList.remove("inactive");
    }
    this.selected_carousel_indices[key] = index;
 
    if (propagate) {
      let listeners = this.carousel_listeners[key];
      for (let listener of listeners) {
        listener(key, index);
      }
    }
  }

  add_carousel_change_listener(key, listener) {
    this.carousel_listeners[key].add(listener);
  }
}

class Benchmarks {
  constructor() {
    this.tables = {};
    this.table_rows = {};
    this.selected_table_rows = {};
    this.row_listeners = {};

    let tables = document.getElementsByClassName("benchmark-table");
    for (let table of tables) {
      let key = table.getAttribute("key");
      if (key === null) continue;
      this.tables[key] = table;
      this.selected_table_rows[key] = null;
    }

    for (let key in this.tables) {
      let table = this.tables[key];
      let rows = [];
      let index = 0;
      for (let elem of table.querySelector("tbody").children) {
        let copy_index = index;
        elem.addEventListener("click", (ev) => {
          ev.preventDefault();
          ev.stopPropagation();
          this.select_row(key, copy_index, true);
        });
        rows.push(elem);
        index++;
      }
      this.table_rows[key] = rows;
    }
    for (let key in this.tables) {
      this.row_listeners[key] = new Set([]);
    }
    for (let key in this.tables) {
      this.select_row(key, 0, false);
    }
  }

  select_row(key, index, propagate) {
    let table_rows = this.table_rows[key];
    let selected_table_row = this.selected_table_rows[key];
    if (selected_table_row !== null && selected_table_row !== index) {
      table_rows[selected_table_row].classList.remove("selected");
    }
    if (selected_table_row !== index) {
      table_rows[index].classList.add("selected");
    }
    this.selected_table_rows[key] = index;
    if (propagate) {
      let listeners = this.row_listeners[key];
      for (let listener of listeners) {
        listener(key, index);
      }
    }
  }

  add_row_change_listener(key, listener) {
    this.row_listeners[key].add(listener);
  }
}

export { Popups, ResponsiveImages, Carousels, Benchmarks };
