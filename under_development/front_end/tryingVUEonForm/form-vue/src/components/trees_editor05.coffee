`/* eslint-disable */`


export class Tree
    @instances = []
    constructor: (tree_container, input_name) ->
        if Tree.instances.length >= 2
            throw Error("can't create more than 2 tree instances")
        else if Tree.instances.length == 1
            @number = 1
        else
            @number = 0
        Object.defineProperty @, "other_instance",
            get: ->
                if Tree.instances.length <= 1
                    return null
                else if Tree.instances.length == 2 and @number == 0
                    return Tree.instances[1]
                else if Tree.instances.length == 2 and @number == 1
                    return Tree.instances[0]
        @highlighted_nodes_ids = []
        @tree_container = tree_container
        @input_node = document.querySelector("input[name=#{input_name}]")
        @background = tree_container.querySelector(".background")
        @foreground = tree_container.querySelector(".foreground")
        root = Receiver.get_root()
        if root != "error"
            @root_object = new Storage(root.name,
                                       Number(root.id),
                                       null,
                                       @)
        else
            @root_object = new Storage("error",
                                       0,
                                       null,
                                       @)
        @root_object.li = @foreground.querySelector("li")
        @root_object.span = @root_object.li.querySelector("span")
        @root_object.span.addEventListener("dblclick", @root_object.open_close)
        @root_object.span.addEventListener("click", @process_click)


        Tree.instances.push(@)
        @frame_maker = new FrameMaker(@)
        @tree_container.addEventListener("mousedown", @tree_container_mouse)
        @tree_container.addEventListener("mouseup", @tree_container_mouse)
        @tree_container.addEventListener("mousemove", @tree_container_mouse)
        @there_was_mousedown = false

    update_field: (new_value) =>
        @input_node.setAttribute("value", JSON.stringify(new_value))

    tree_container_mouse: (event) =>
        if event.target.nodeName != "SPAN"
            if event.type == "mousedown"
                @there_was_mousedown = true
            else if event.type == "mousemove"
                @there_was_mousedown = false
            else if event.type == "mouseup" and @there_was_mousedown
                for id_of_node in @highlighted_nodes_ids
                    node = @foreground.querySelector(
                        "span[data-storage_node_id='#{id_of_node}']"
                    )
                    node.classList.remove("highlighted")
                @highlighted_nodes_ids = []
                @update_field(@highlighted_nodes_ids)
                @there_was_mousedown = false

    highlight: (node_id) =>
        if @highlighted_nodes_ids.indexOf(node_id) == -1
            @highlighted_nodes_ids.push(node_id)
            @update_field(@highlighted_nodes_ids)
            node = @foreground.querySelector(
                "span[data-storage_node_id='#{node_id}']"
            )
            node.classList.add("highlighted")

    unhighlight: (node_id) =>
        if @highlighted_nodes_ids.indexOf(node_id) != -1
            index_in_array = @highlighted_nodes_ids.indexOf(node_id)
            @highlighted_nodes_ids.splice(index_in_array, 1)
            @update_field(@highlighted_nodes_ids)
            node = @foreground.querySelector(
                "span[data-storage_node_id='#{node_id}']"
            )
            node.classList.remove("highlighted")

    highlight_only_this: (node_id) =>
        for id_of_node in @highlighted_nodes_ids
            node = @foreground.querySelector(
                "span[data-storage_node_id='#{id_of_node}']"
            )
            node.classList.remove("highlighted")
        @highlighted_nodes_ids = []
        @update_field(@highlighted_nodes_ids)
        @highlight(node_id)

    process_click: (event) =>
        if event.target.classList.contains("highlighted")
            if event.shiftKey or event.ctrlKey
                @highlighted_shift_or_ctrl(event)
            else
                @highlighted_no_key(event)
        else
            if event.shiftKey
                @unhighlighted_shift(event)
            else if event.ctrlKey
                @unhighlighted_ctrl(event)
            else
                @unhighlighted_no_key(event)

    highlighted_shift_or_ctrl: (event) =>
        @unhighlight(event.target.dataset.storage_node_id)

    highlighted_no_key: (event) =>
        if @highlighted_nodes_ids.length == 1
            @unhighlight(event.target.dataset.storage_node_id)
        else if @highlighted_nodes_ids.length > 1
            @highlight_only_this(event.target.dataset.storage_node_id)

    unhighlighted_shift: (event) =>
        the_ul = @foreground.querySelector("ul")
        levels = [[the_ul]]
        while levels[levels.length - 1].length != 0
            levels = @process_levels(levels)
        uls_spans_level = null
        for level in levels
            if level.indexOf(event.target) != -1
                uls_spans_level = level
                break
        spans_level_list = []
        for node in uls_spans_level
            if node.tagName == "SPAN"
                spans_level_list.push(node)
        @process_span_list(spans_level_list, event.target)

    process_levels: (levels) ->
        last_level = levels[levels.length - 1]
        new_level = []
        for item in last_level
            children_arr = Array.from(item.children)
            Array.prototype.push.apply(new_level, children_arr)
        levels.push(new_level)
        return levels

    process_span_list: (span_list, event_target) =>
        will_continue = false
        for node in span_list
            if node.classList.contains("highlighted")
                will_continue = true
                break
        if not will_continue
            return null
        @highlight_domain(span_list, event_target)

    highlight_domain: (span_list, event_target) =>
        domain_of_numbers = []
        target_number = span_list.indexOf(event_target)
        for number in [target_number..0]
            if span_list[number].classList.contains("highlighted")
                break
            else
                domain_of_numbers.push(number)
                continue
        if target_number < span_list.length - 1
            for number in [target_number + 1..span_list.length - 1]
                if span_list[number].classList.contains("highlighted")
                    break
                else
                    domain_of_numbers.push(number)
                    continue
        for number in domain_of_numbers
            @highlight(span_list[number].dataset.storage_node_id)


    unhighlighted_ctrl: (event) =>
        @highlight(event.target.dataset.storage_node_id)

    unhighlighted_no_key: (event) =>
        @highlight_only_this(event.target.dataset.storage_node_id)


class Chemical
    @chemicals_and_storages = {}
    constructor: (name, id, parent, tree) ->
        @name = name
        @id = id
        @parent = parent
        @tree = tree
        @li = null
        @span = null
        Chemical.chemicals_and_storages[id] = @


class Storage extends Chemical
    constructor: (name, id, parent, tree) ->
        super(name, id, parent, tree)
        @children = []
        @level = null
        @is_terminal = false
        @is_open = false

    open_close: (event) =>
        @tree.unhighlight(event.target.dataset.storage_node_id)
        if @is_open and event.target == @span
            ul = @li.querySelector("ul")
            ul.remove()
            @children = []
            @is_open = false
            @li.classList.remove("open")
            @li.classList.add("closed")
        else
            if event.target == @span
                children = Receiver.get_children(@id)
                @create_children_from_list(children)
                if JSON.stringify(children) != "{}"
                    @is_open = true
                    @li.classList.remove("closed")
                    @li.classList.add("open")
        @tree.frame_maker.destructor()
        @tree.frame_maker = new FrameMaker(@tree)

    create_children_from_list: (children) ->
        ul = document.createElement("ul")
        @li.append(ul)
        for id of children
            name = children[id]
            if isNaN(id)
                child = new Chemical(name, id, @, @tree)
            else
                child = new Storage(name, Number(id), @, @tree)
            @children.push(child)
            li = document.createElement("li")
            span = document.createElement("span")
            span.textContent = name
            span.setAttribute("data-storage_node_id", id)
            li.append(span)
            ul.append(li)
            child.li = li
            child.span = span
            if child instanceof Storage
                span.addEventListener("dblclick", child.open_close)
                span.addEventListener("click", @tree.process_click)
                li.classList.add("closed")
            else
                span.addEventListener("click", @tree.process_click)
                li.classList.add("chemical")


class Receiver
    @content = {}
    # content format: {1: {name: "One", parent: 0, terminal: false}}
    # where 1 is storage id
    @debug = true

#    @call: (parent_id) ->
#        result = {}
#        for key of @content
#            if @content[key].parent == parent_id
#                result[key] = @content[key].name
#        return result
    @csrf: () ->
        if @debug
            return ""
        else
            csrfContainer = document.querySelector("#csrf")
            csrfInput = csrfContainer.querySelector("input")
            return csrfInput.getAttribute("value")


    @tree_address: () ->
        if @debug
            return "http://127.0.0.1:5000/"
        else
            window.location.href


    @get_children: (parent_id) ->
        if not `parent_id in this.content`
            throw Error("No such parent_id in @content")
        if @content[parent_id].terminal == true
            return {}
        form_to_send = new FormData()
        form_to_send.append("give_children_of", parent_id)
        xhr = new XMLHttpRequest()
        xhr.open("POST", @tree_address(), false)
        xhr.setRequestHeader("X-CSRFToken", @csrf())
        try
            xhr.send(form_to_send)
            if xhr.status == 200
                received_str = xhr.response
                result = JSON.parse(received_str)
                returned_obj = {}
                for id of result
                    returned_obj[id] = result[id][0]
                    @content[id] = {
                        name: result[id][0],
                        parent: parent_id,
                        terminal: result[id][1]
                    }
                return returned_obj
            else
                return "error"
        catch
            return "error"


    @record_creation: () ->
        null

    @get_root: () ->
        form_to_send = new FormData()
        form_to_send.append("give_root", "")
        xhr = new XMLHttpRequest()
        xhr.open("POST", @tree_address(), false)
        xhr.setRequestHeader("X-CSRFToken", @csrf())
        try
            xhr.send(form_to_send)
            if xhr.status == 200
                received_str = xhr.response
                received_obj = JSON.parse(received_str)
                root_id = Object.keys(received_obj)[0]
                root_name = received_obj[root_id][0]
                root_terminal = received_obj[root_id][1]
                Receiver.content[root_id] = {
                    name: root_name,
                    parent: null,
                    terminal: root_terminal,
                }
                return {id: root_id, name: root_name}
            else
                return "error"
        catch
            return "error"


class FrameMaker
    constructor: (tree) ->
        @tree = tree
        @anchor = {x: 0, y: 0}
        @background = tree.background
        @foreground = tree.foreground
        @foreground.addEventListener("mousedown", @send_event)
        @foreground.addEventListener("mouseup", @send_event)
        @foreground.addEventListener("mousemove", @send_event)
        @foreground.addEventListener("mouseleave", @send_event)
        @back_coords = @background.getBoundingClientRect()
        @background.addEventListener("mousedown", @mousedown_processor)
        @inner_frame = null
        @li_list = @make_li_list()

    destructor: () =>
        @foreground.removeEventListener("mousedown", @send_event)
        @foreground.removeEventListener("mouseup", @send_event)
        @foreground.removeEventListener("mousemove", @send_event)
        @foreground.removeEventListener("mouseleave", @send_event)
        @background.removeEventListener("mousedown", @mousedown_processor)
        @anchor = null
        @background = null
        @foreground = null
        @back_coords = null
        @inner_frame = null
        @li_list = null

    make_li_list: () =>
        span_list = []
        all_spans = @foreground.querySelectorAll("span")
        for element in all_spans
            list_point = new ListPoint(element, @tree)
            span_list.push(list_point)
        return span_list

    send_event: (event) =>
        new_event = new MouseEvent(event.type, {
            bubbles: false
            cancelable: false
            clientX: event.clientX
            clientY: event.clientY
        })
        @background.dispatchEvent(new_event)

    mousedown_processor: (event) =>
        @anchor.x = event.clientX - @back_coords.left
        @anchor.y = event.clientY - @back_coords.top
        if @inner_frame
            @inner_frame.remove()
        @inner_frame = document.createElement("div")
        @background.prepend(@inner_frame)
        style_value = ("margin-top: #{@anchor.y}px; margin-left: " +
            "#{@anchor.x}px; width: #{0}px; height: #{0}px;")
        @inner_frame.setAttribute("style", style_value)
        @inner_frame.classList.add("figure")
        @background.addEventListener("mousemove", @mousemove_processor)
        @background.addEventListener("mouseup", @mouseup_leave_processor)
        @background.addEventListener("mouseleave", @mouseup_leave_processor)

    mousemove_processor: (event) =>
        x = event.clientX - @back_coords.left
        y = event.clientY - @back_coords.top
        margin_left = Math.min(x, @anchor.x)
        margin_top = Math.min(y, @anchor.y)
        width = Math.max(x, @anchor.x) - margin_left
        height = Math.max(y, @anchor.y) - margin_top
        style_value = ("margin-top: #{margin_top}px; margin-left: " +
            "#{margin_left}px; " +
            "width: #{width}px; height: #{height}px;")
        @inner_frame.setAttribute("style", style_value)
        @check_for_intersections(margin_left,
            margin_top,
            margin_left + width,
            margin_top + height)

    check_for_intersections: (left, top, right, bottom) =>
        for list_point in @li_list
            list_point.check(left, top, right, bottom, @back_coords)

    mouseup_leave_processor: (event) =>
        @inner_frame.remove()
        @inner_frame = null
        @background.removeEventListener("mousemove", @mousemove_processor)
        @background.removeEventListener("mouseup", @mouseup_leave_processor)
        @background.removeEventListener("mouseleave", @mouseup_leave_processor)


class ListPoint
    constructor: (node, tree) ->
        @node = node
        @tree = tree
        @rectangle = node.getBoundingClientRect()
        @highlighted = false

    check: (left, top, right, bottom, back_coords) =>
        if (top < @rectangle.top - back_coords.top < bottom or
            top < @rectangle.bottom - back_coords.top < bottom) and
            (left < @rectangle.left - back_coords.left < right or
                left < @rectangle.right - back_coords.left < right)
            if @highlighted == false
                @node.classList.add("highlighted")
                @highlighted = true
                storage_node_id = @node.dataset.storage_node_id
                @tree.highlight(storage_node_id)
        else
            if @highlighted == true
                @node.classList.remove("highlighted")
                @highlighted = false
                storage_node_id = @node.dataset.storage_node_id
                @tree.unhighlight(storage_node_id)
