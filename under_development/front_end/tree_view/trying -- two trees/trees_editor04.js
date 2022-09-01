// Generated by CoffeeScript 2.6.1
(function() {
  var Button, Chemical, FrameMaker, InfoPanel, ListPoint, PageManager, Receiver, Separator, Storage, Tree, page_manager,
    boundMethodCheck = function(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new Error('Bound instance method accessed before binding'); } };

  InfoPanel = class InfoPanel {
    constructor(node) {
      var i, len, ref, triangle;
      this.show_palette = this.show_palette.bind(this);
      this.show_button = this.show_button.bind(this);
      this.change_parent_flex_direction = this.change_parent_flex_direction.bind(this);
      this.change_position = this.change_position.bind(this);
      this.node = node;
      this.position = "top";
      this.button = node.querySelector("button");
      this.palette = node.querySelector("div.position_palette");
      this.button.addEventListener("click", this.show_palette);
      this.palette.addEventListener("mouseleave", this.show_button);
      this.triangle_up = node.querySelector("div.triangle_up");
      this.triangle_down = node.querySelector("div.triangle_down");
      this.triangle_left = node.querySelector("div.triangle_left");
      this.triangle_right = node.querySelector("div.triangle_right");
      ref = [this.triangle_up, this.triangle_down, this.triangle_left, this.triangle_right];
      for (i = 0, len = ref.length; i < len; i++) {
        triangle = ref[i];
        triangle.addEventListener("click", this.change_position);
      }
    }

    show_palette(event) {
      this.button.classList.add("invisible");
      return this.palette.classList.remove("invisible");
    }

    show_button(event) {
      this.button.classList.remove("invisible");
      return this.palette.classList.add("invisible");
    }

    change_parent_flex_direction(new_value) {
      return this.node.parentNode.setAttribute("style", `flex-direction: ${new_value};`);
    }

    change_position(event) {
      if (event.target === this.triangle_up && this.position !== "top") {
        this.change_parent_flex_direction("column");
        return this.position = "top";
      } else if (event.target === this.triangle_left && this.position !== "left") {
        this.change_parent_flex_direction("row");
        return this.position = "left";
      } else if (event.target === this.triangle_down && this.position !== "bottom") {
        this.change_parent_flex_direction("column-reverse");
        return this.position = "bottom";
      } else if (event.target === this.triangle_right && this.position !== "right") {
        this.change_parent_flex_direction("row-reverse");
        return this.position = "right";
      }
    }

  };

  Separator = class Separator {
    constructor(node) {
      this.start_following = this.start_following.bind(this);
      this.follow = this.follow.bind(this);
      this.stop_following = this.stop_following.bind(this);
      this.initial_x = null;
      this.initial_y = null;
      this.node = node;
      this.previous_node = this.node.previousElementSibling;
      this.next_node = this.node.nextElementSibling;
      this.node.addEventListener("dragstart", this.start_following);
    }

    start_following(event) {
      var rect;
      this.previous_node.addEventListener("dragover", this.follow);
      this.previous_node.addEventListener("dragend", this.stop_following);
      this.next_node.addEventListener("dragover", this.follow);
      this.next_node.addEventListener("dragend", this.stop_following);
      this.initial_x = event.clientX;
      this.initial_y = event.clientY;
      rect = this.previous_node.getBoundingClientRect();
      if (rect.height > rect.width) {
        this.size = Math.round(rect.width);
      } else {
        this.size = Math.round(rect.height);
      }
      return this.previous_node.setAttribute("style", `flex-basis: ${this.size}px;`);
    }

    follow(event) {
      var delta, new_size, prev_rect, rect, style_value;
      rect = this.node.getBoundingClientRect();
      prev_rect = this.previous_node.getBoundingClientRect();
      if (rect.height > rect.width) {
        if (prev_rect.x > rect.x) {
          delta = event.clientX - this.initial_x;
          new_size = Math.round(this.size - delta);
        } else {
          delta = event.clientX - this.initial_x;
          new_size = Math.round(this.size + delta);
        }
      } else {
        if (prev_rect.y > rect.y) {
          delta = event.clientY - this.initial_y;
          new_size = Math.round(this.size - delta);
        } else {
          delta = event.clientY - this.initial_y;
          new_size = Math.round(this.size + delta);
        }
      }
      style_value = `flex-basis: ${new_size}px;`;
      return this.previous_node.setAttribute("style", style_value);
    }

    stop_following(event) {
      this.next_node.removeEventListener("dragover", this.follow);
      this.previous_node.removeEventListener("dragover", this.follow);
      this.next_node.removeEventListener("dragend", this.stop_following);
      return this.previous_node.removeEventListener("dragend", this.stop_following);
    }

  };

  Tree = (function() {
    class Tree {
      constructor(tree_container) {
        this.create_buttons = this.create_buttons.bind(this);
        this.tree_container_mouse = this.tree_container_mouse.bind(this);
        this.highlight = this.highlight.bind(this);
        this.unhighlight = this.unhighlight.bind(this);
        this.highlight_only_this = this.highlight_only_this.bind(this);
        this.process_click = this.process_click.bind(this);
        this.highlighted_shift_or_ctrl = this.highlighted_shift_or_ctrl.bind(this);
        this.highlighted_no_key = this.highlighted_no_key.bind(this);
        this.unhighlighted_shift = this.unhighlighted_shift.bind(this);
        this.process_span_list = this.process_span_list.bind(this);
        this.highlight_domain = this.highlight_domain.bind(this);
        this.unhighlighted_ctrl = this.unhighlighted_ctrl.bind(this);
        this.unhighlighted_no_key = this.unhighlighted_no_key.bind(this);
        if (Tree.instances.length >= 2) {
          throw Error("can't create more than 2 tree instances");
        } else if (Tree.instances.length === 1) {
          this.number = 1;
        } else {
          this.number = 0;
        }
        Object.defineProperty(this, "other_instance", {
          get: function() {
            if (Tree.instances.length <= 1) {
              return null;
            } else if (Tree.instances.length === 2 && this.number === 0) {
              return Tree.instances[1];
            } else if (Tree.instances.length === 2 && this.number === 1) {
              return Tree.instances[0];
            }
          }
        });
        this.buttons = null;
        this.create_buttons();
        this.highlighted_nodes_ids = [];
        this.tree_container = tree_container;
        this.background = tree_container.querySelector(".background");
        this.foreground = tree_container.querySelector(".foreground");
        this.root_object = new Storage(this.foreground.dataset.root_name, Number(this.foreground.dataset.root_id), null, this);
        this.root_object.li = this.foreground.querySelector("li");
        this.root_object.span = this.root_object.li.querySelector("span");
        this.root_object.span.addEventListener("dblclick", this.root_object.open_close);
        this.root_object.span.addEventListener("click", this.process_click);
        Tree.instances.push(this);
        this.frame_maker = new FrameMaker(this);
        this.tree_container.addEventListener("mousedown", this.tree_container_mouse);
        this.tree_container.addEventListener("mouseup", this.tree_container_mouse);
        this.tree_container.addEventListener("mousemove", this.tree_container_mouse);
        this.there_was_mousedown = false;
      }

      create_buttons() {
        return this.buttons = {
          "add_storage": null,
          "add_chemical": null,
          "view_chemical": null,
          "edit": null,
          "cut": null,
          "paste": null,
          "move": null,
          "delete_storage": null,
          "move_to_the_left": null,
          "move_to_the_right": null,
          "close": null
        };
      }

      tree_container_mouse(event) {
        var i, id_of_node, len, node, ref;
        if (event.target.nodeName !== "SPAN") {
          if (event.type === "mousedown") {
            return this.there_was_mousedown = true;
          } else if (event.type === "mousemove") {
            return this.there_was_mousedown = false;
          } else if (event.type === "mouseup" && this.there_was_mousedown) {
            ref = this.highlighted_nodes_ids;
            for (i = 0, len = ref.length; i < len; i++) {
              id_of_node = ref[i];
              node = this.foreground.querySelector(`span[data-storage_node_id='${id_of_node}']`);
              node.classList.remove("highlighted");
            }
            this.highlighted_nodes_ids = [];
            return this.there_was_mousedown = false;
          }
        }
      }

      highlight(node_id) {
        var node;
        if (this.highlighted_nodes_ids.indexOf(node_id) === -1) {
          this.highlighted_nodes_ids.push(node_id);
          node = this.foreground.querySelector(`span[data-storage_node_id='${node_id}']`);
          return node.classList.add("highlighted");
        }
      }

      unhighlight(node_id) {
        var index_in_array, node;
        if (this.highlighted_nodes_ids.indexOf(node_id) !== -1) {
          index_in_array = this.highlighted_nodes_ids.indexOf(node_id);
          this.highlighted_nodes_ids.splice(index_in_array, 1);
          node = this.foreground.querySelector(`span[data-storage_node_id='${node_id}']`);
          return node.classList.remove("highlighted");
        }
      }

      highlight_only_this(node_id) {
        var i, id_of_node, len, node, ref;
        ref = this.highlighted_nodes_ids;
        for (i = 0, len = ref.length; i < len; i++) {
          id_of_node = ref[i];
          node = this.foreground.querySelector(`span[data-storage_node_id='${id_of_node}']`);
          node.classList.remove("highlighted");
        }
        this.highlighted_nodes_ids = [];
        return this.highlight(node_id);
      }

      process_click(event) {
        if (event.target.classList.contains("highlighted")) {
          if (event.shiftKey || event.ctrlKey) {
            return this.highlighted_shift_or_ctrl(event);
          } else {
            return this.highlighted_no_key(event);
          }
        } else {
          if (event.shiftKey) {
            return this.unhighlighted_shift(event);
          } else if (event.ctrlKey) {
            return this.unhighlighted_ctrl(event);
          } else {
            return this.unhighlighted_no_key(event);
          }
        }
      }

      highlighted_shift_or_ctrl(event) {
        return this.unhighlight(event.target.dataset.storage_node_id);
      }

      highlighted_no_key(event) {
        if (this.highlighted_nodes_ids.length === 1) {
          return this.unhighlight(event.target.dataset.storage_node_id);
        } else if (this.highlighted_nodes_ids.length > 1) {
          return this.highlight_only_this(event.target.dataset.storage_node_id);
        }
      }

      unhighlighted_shift(event) {
        var i, j, len, len1, level, levels, node, spans_level_list, the_ul, uls_spans_level;
        the_ul = this.foreground.querySelector("ul");
        levels = [[the_ul]];
        while (levels[levels.length - 1].length !== 0) {
          levels = this.process_levels(levels);
        }
        uls_spans_level = null;
        for (i = 0, len = levels.length; i < len; i++) {
          level = levels[i];
          if (level.indexOf(event.target) !== -1) {
            uls_spans_level = level;
            break;
          }
        }
        spans_level_list = [];
        for (j = 0, len1 = uls_spans_level.length; j < len1; j++) {
          node = uls_spans_level[j];
          if (node.tagName === "SPAN") {
            spans_level_list.push(node);
          }
        }
        return this.process_span_list(spans_level_list, event.target);
      }

      process_levels(levels) {
        var children_arr, i, item, last_level, len, new_level;
        last_level = levels[levels.length - 1];
        new_level = [];
        for (i = 0, len = last_level.length; i < len; i++) {
          item = last_level[i];
          children_arr = Array.from(item.children);
          Array.prototype.push.apply(new_level, children_arr);
        }
        levels.push(new_level);
        return levels;
      }

      process_span_list(span_list, event_target) {
        var i, len, node, will_continue;
        will_continue = false;
        for (i = 0, len = span_list.length; i < len; i++) {
          node = span_list[i];
          if (node.classList.contains("highlighted")) {
            will_continue = true;
            break;
          }
        }
        if (!will_continue) {
          return null;
        }
        return this.highlight_domain(span_list, event_target);
      }

      highlight_domain(span_list, event_target) {
        var domain_of_numbers, i, j, k, len, number, ref, ref1, ref2, results, target_number;
        domain_of_numbers = [];
        target_number = span_list.indexOf(event_target);
        for (number = i = ref = target_number; (ref <= 0 ? i <= 0 : i >= 0); number = ref <= 0 ? ++i : --i) {
          if (span_list[number].classList.contains("highlighted")) {
            break;
          } else {
            domain_of_numbers.push(number);
            continue;
          }
        }
        if (target_number < span_list.length - 1) {
          for (number = j = ref1 = target_number + 1, ref2 = span_list.length - 1; (ref1 <= ref2 ? j <= ref2 : j >= ref2); number = ref1 <= ref2 ? ++j : --j) {
            if (span_list[number].classList.contains("highlighted")) {
              break;
            } else {
              domain_of_numbers.push(number);
              continue;
            }
          }
        }
        results = [];
        for (k = 0, len = domain_of_numbers.length; k < len; k++) {
          number = domain_of_numbers[k];
          results.push(this.highlight(span_list[number].dataset.storage_node_id));
        }
        return results;
      }

      unhighlighted_ctrl(event) {
        return this.highlight(event.target.dataset.storage_node_id);
      }

      unhighlighted_no_key(event) {
        return this.highlight_only_this(event.target.dataset.storage_node_id);
      }

    };

    Tree.instances = [];

    return Tree;

  }).call(this);

  Chemical = (function() {
    class Chemical {
      constructor(name, id, parent, tree) {
        this.name = name;
        this.id = id;
        this.parent = parent;
        this.tree = tree;
        this.li = null;
        this.span = null;
        Chemical.chemicals_and_storages[id] = this;
      }

    };

    Chemical.chemicals_and_storages = {};

    return Chemical;

  }).call(this);

  Storage = class Storage extends Chemical {
    constructor(name, id, parent, tree) {
      super(name, id, parent, tree);
      this.open_close = this.open_close.bind(this);
      this.children = [];
      this.level = null;
      this.is_terminal = false;
      this.is_open = false;
    }

    open_close(event) {
      var children, ul;
      boundMethodCheck(this, Storage);
      this.tree.unhighlight(event.target.dataset.storage_node_id);
      if (this.is_open && event.target === this.span) {
        ul = this.li.querySelector("ul");
        ul.remove();
        this.children = [];
        this.is_open = false;
        this.li.classList.remove("open");
        this.li.classList.add("closed");
      } else {
        if (event.target === this.span) {
          children = Receiver.call(this.id);
          this.create_children_from_list(children);
          if (JSON.stringify(children) !== "{}") {
            this.is_open = true;
            this.li.classList.remove("closed");
            this.li.classList.add("open");
          }
        }
      }
      this.tree.frame_maker.destructor();
      return this.tree.frame_maker = new FrameMaker(this.tree);
    }

    create_children_from_list(children) {
      var child, id, li, name, results, span, ul;
      ul = document.createElement("ul");
      this.li.append(ul);
      results = [];
      for (id in children) {
        name = children[id];
        if (isNaN(id)) {
          child = new Chemical(name, id, this, this.tree);
        } else {
          child = new Storage(name, Number(id), this, this.tree);
        }
        this.children.push(child);
        li = document.createElement("li");
        span = document.createElement("span");
        span.textContent = name;
        span.setAttribute("data-storage_node_id", id);
        li.append(span);
        ul.append(li);
        child.li = li;
        child.span = span;
        if (child instanceof Storage) {
          span.addEventListener("dblclick", child.open_close);
          span.addEventListener("click", this.tree.process_click);
          results.push(li.classList.add("closed"));
        } else {
          span.addEventListener("click", this.tree.process_click);
          results.push(li.classList.add("chemical"));
        }
      }
      return results;
    }

  };

  Button = (function() {
    class Button {
      constructor(tree) {
        var container_container, selector;
        this.press_the_button = this.press_the_button.bind(this);
        // Not implemented
        this.update_activity_status = this.update_activity_status.bind(this);
        // Not implemented
        this.check_if_need_activation = this.check_if_need_activation.bind(this);
        // Not implemented
        this.activate = this.activate.bind(this);
        this.deactivate = this.deactivate.bind(this);
        this.tree = tree;
        this.active = true;
        if (this instanceof Button) {
          throw Error("Can't instantiate abstract class");
        }
        if (Object.hasOwn(this.tree.buttons, this.name) && this.tree.buttons[this.name] === null) {
          this.tree.buttons = this;
        } else {
          throw Error("One such button already created");
        }
        container_container = this.tree.tree_container.parentNode;
        selector = `button[title='${this.title}']`;
        this.html_button = container_container.querySelector(selector);
        if (this.html_button.hasAttribute("disabled")) {
          this.active = false;
        }
        this.html_button.addEventListener("click", this.press_the_button);
      }

      press_the_button() {
        return null;
      }

      update_activity_status() {
        return null;
      }

      check_if_need_activation() {
        return null;
      }

      activate() {
        return this.html_button.setAttribute("disabled", "disabled");
      }

      deactivate() {
        return this.html_button.removeAttribute("disabled");
      }

    };

    // Abstract key class
    Button.name = "";

    Button.title = "";

    return Button;

  }).call(this);

  Receiver = (function() {
    class Receiver {
      static call(parent_id) {
        var key, result;
        result = {};
        for (key in this.content) {
          if (this.content[key].parent === parent_id) {
            result[key] = this.content[key].name;
          }
        }
        return result;
      }

      static record_creation() {
        return null;
      }

    };

    Receiver.content = {
      1: {
        name: "One",
        parent: 0
      },
      2: {
        name: "Two",
        parent: 0
      },
      3: {
        name: "Three",
        parent: 0
      },
      4: {
        name: "Four",
        parent: 2
      },
      "chem5": {
        name: "Five",
        parent: 4
      }
    };

    return Receiver;

  }).call(this);

  FrameMaker = class FrameMaker {
    constructor(tree) {
      this.destructor = this.destructor.bind(this);
      this.make_li_list = this.make_li_list.bind(this);
      this.send_event = this.send_event.bind(this);
      this.mousedown_processor = this.mousedown_processor.bind(this);
      this.mousemove_processor = this.mousemove_processor.bind(this);
      this.check_for_intersections = this.check_for_intersections.bind(this);
      this.mouseup_leave_processor = this.mouseup_leave_processor.bind(this);
      this.tree = tree;
      this.anchor = {
        x: 0,
        y: 0
      };
      this.background = tree.background;
      this.foreground = tree.foreground;
      this.foreground.addEventListener("mousedown", this.send_event);
      this.foreground.addEventListener("mouseup", this.send_event);
      this.foreground.addEventListener("mousemove", this.send_event);
      this.foreground.addEventListener("mouseleave", this.send_event);
      this.back_coords = this.background.getBoundingClientRect();
      this.background.addEventListener("mousedown", this.mousedown_processor);
      this.inner_frame = null;
      this.li_list = this.make_li_list();
    }

    destructor() {
      this.foreground.removeEventListener("mousedown", this.send_event);
      this.foreground.removeEventListener("mouseup", this.send_event);
      this.foreground.removeEventListener("mousemove", this.send_event);
      this.foreground.removeEventListener("mouseleave", this.send_event);
      this.background.removeEventListener("mousedown", this.mousedown_processor);
      this.anchor = null;
      this.background = null;
      this.foreground = null;
      this.back_coords = null;
      this.inner_frame = null;
      return this.li_list = null;
    }

    make_li_list() {
      var all_spans, element, i, len, list_point, span_list;
      span_list = [];
      all_spans = this.foreground.querySelectorAll("span");
      for (i = 0, len = all_spans.length; i < len; i++) {
        element = all_spans[i];
        list_point = new ListPoint(element, this.tree);
        span_list.push(list_point);
      }
      return span_list;
    }

    send_event(event) {
      var new_event;
      new_event = new MouseEvent(event.type, {
        bubbles: false,
        cancelable: false,
        clientX: event.clientX,
        clientY: event.clientY
      });
      return this.background.dispatchEvent(new_event);
    }

    mousedown_processor(event) {
      var style_value;
      this.anchor.x = event.clientX - this.back_coords.left;
      this.anchor.y = event.clientY - this.back_coords.top;
      if (this.inner_frame) {
        this.inner_frame.remove();
      }
      this.inner_frame = document.createElement("div");
      this.background.prepend(this.inner_frame);
      style_value = `margin-top: ${this.anchor.y}px; margin-left: ` + `${this.anchor.x}px; width: ${0}px; height: ${0}px;`;
      this.inner_frame.setAttribute("style", style_value);
      this.inner_frame.classList.add("figure");
      this.background.addEventListener("mousemove", this.mousemove_processor);
      this.background.addEventListener("mouseup", this.mouseup_leave_processor);
      return this.background.addEventListener("mouseleave", this.mouseup_leave_processor);
    }

    mousemove_processor(event) {
      var height, margin_left, margin_top, style_value, width, x, y;
      x = event.clientX - this.back_coords.left;
      y = event.clientY - this.back_coords.top;
      margin_left = Math.min(x, this.anchor.x);
      margin_top = Math.min(y, this.anchor.y);
      width = Math.max(x, this.anchor.x) - margin_left;
      height = Math.max(y, this.anchor.y) - margin_top;
      style_value = `margin-top: ${margin_top}px; margin-left: ` + `${margin_left}px; ` + `width: ${width}px; height: ${height}px;`;
      this.inner_frame.setAttribute("style", style_value);
      return this.check_for_intersections(margin_left, margin_top, margin_left + width, margin_top + height);
    }

    check_for_intersections(left, top, right, bottom) {
      var i, len, list_point, ref, results;
      ref = this.li_list;
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        list_point = ref[i];
        results.push(list_point.check(left, top, right, bottom, this.back_coords));
      }
      return results;
    }

    mouseup_leave_processor(event) {
      this.inner_frame.remove();
      this.inner_frame = null;
      this.background.removeEventListener("mousemove", this.mousemove_processor);
      this.background.removeEventListener("mouseup", this.mouseup_leave_processor);
      return this.background.removeEventListener("mouseleave", this.mouseup_leave_processor);
    }

  };

  ListPoint = class ListPoint {
    constructor(node, tree) {
      this.check = this.check.bind(this);
      this.node = node;
      this.tree = tree;
      this.rectangle = node.getBoundingClientRect();
      this.highlighted = false;
    }

    check(left, top, right, bottom, back_coords) {
      var ref, ref1, ref2, ref3, storage_node_id;
      if (((top < (ref = this.rectangle.top - back_coords.top) && ref < bottom) || (top < (ref1 = this.rectangle.bottom - back_coords.top) && ref1 < bottom)) && ((left < (ref2 = this.rectangle.left - back_coords.left) && ref2 < right) || (left < (ref3 = this.rectangle.right - back_coords.left) && ref3 < right))) {
        if (this.highlighted === false) {
          this.node.classList.add("highlighted");
          this.highlighted = true;
          storage_node_id = this.node.dataset.storage_node_id;
          return this.tree.highlight(storage_node_id);
        }
      } else {
        if (this.highlighted === true) {
          this.node.classList.remove("highlighted");
          this.highlighted = false;
          storage_node_id = this.node.dataset.storage_node_id;
          return this.tree.unhighlight(storage_node_id);
        }
      }
    }

  };

  PageManager = class PageManager {
    constructor() {
      var i, len, new_separator, ref, separator;
      this.info = document.querySelector("div.info");
      this.info_panel = new InfoPanel(this.info);
      this.separators = [];
      ref = document.querySelectorAll("div.separator");
      for (i = 0, len = ref.length; i < len; i++) {
        separator = ref[i];
        new_separator = new Separator(separator);
        this.separators.push(new_separator);
      }
      this.tree_container = document.querySelector("div.tree_container");
      this.tree = [];
      this.tree.push(new Tree(this.tree_container));
    }

  };

  page_manager = new PageManager();

}).call(this);

//# sourceMappingURL=trees_editor04.js.map
