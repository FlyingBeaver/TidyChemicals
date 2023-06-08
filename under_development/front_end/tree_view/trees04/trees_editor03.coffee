class InfoPanel
    constructor: (node) ->
        @node = node
        @position = "top"
        @button = node.querySelector("button")
        @palette = node.querySelector("div.position_palette")
        @button.addEventListener("click", @show_palette)
        @palette.addEventListener("mouseleave", @show_button)

        @triangle_up = node.querySelector("div.triangle_up")
        @triangle_down = node.querySelector("div.triangle_down")
        @triangle_left = node.querySelector("div.triangle_left")
        @triangle_right = node.querySelector("div.triangle_right")

        for triangle in [@triangle_up, @triangle_down, 
                         @triangle_left, @triangle_right]
            triangle.addEventListener("click", @change_position)

    show_palette: (event) =>
        @button.classList.add("invisible")
        @palette.classList.remove("invisible")

    show_button: (event) =>
        @button.classList.remove("invisible")
        @palette.classList.add("invisible")

    change_parent_flex_direction: (new_value) =>
        @node.parentNode.setAttribute("style", "flex-direction: #{new_value};")

    change_position: (event) =>
        if event.target == @triangle_up and @position != "top"
            @change_parent_flex_direction("column")
            @position = "top"
        else if event.target == @triangle_left and @position != "left"
            @change_parent_flex_direction("row")
            @position = "left"
        else if event.target == @triangle_down and @position != "bottom"
            @change_parent_flex_direction("column-reverse")
            @position = "bottom"
        else if event.target == @triangle_right and @position != "right"
            @change_parent_flex_direction("row-reverse")
            @position = "right"


class Separator
    constructor: (node) ->
        @initial_x = null
        @initial_y = null
        @node = node
        @previous_node = @node.previousElementSibling
        @next_node = @node.nextElementSibling
        @node.addEventListener("dragstart", @start_following)

    start_following: (event) =>
        @previous_node.addEventListener("dragover", @follow)
        @previous_node.addEventListener("dragend", @stop_following)
        @next_node.addEventListener("dragover", @follow)
        @next_node.addEventListener("dragend", @stop_following)
        @initial_x = event.clientX
        @initial_y = event.clientY
        rect = @previous_node.getBoundingClientRect()
        if rect.height > rect.width
            @size = Math.round(rect.width)
        else
            @size = Math.round(rect.height)
        @previous_node.setAttribute("style", "flex-basis: #{@size}px;")

    follow: (event) =>
        rect = @node.getBoundingClientRect()
        prev_rect = @previous_node.getBoundingClientRect()
        if rect.height > rect.width
            if prev_rect.x > rect.x
                delta = event.clientX - @initial_x
                new_size = Math.round(@size - delta)
            else
                delta = event.clientX - @initial_x
                new_size = Math.round(@size + delta)
        else
            if prev_rect.y > rect.y
                delta = event.clientY - @initial_y
                new_size = Math.round(@size - delta)
            else
                delta = event.clientY - @initial_y
                new_size = Math.round(@size + delta)
        style_value = "flex-basis: #{new_size}px;"
        @previous_node.setAttribute("style", style_value)

    stop_following: (event) =>
        @next_node.removeEventListener("dragover", @follow)
        @previous_node.removeEventListener("dragover", @follow)
        @next_node.removeEventListener("dragend", @stop_following)
        @previous_node.removeEventListener("dragend", @stop_following)


class Starter
    constructor: () ->
        @info = document.querySelector("div.info")
        @info_panel = new InfoPanel(@info)
        @separators = []
        for separator in document.querySelectorAll("div.separator")
            new_separator = new Separator(separator)
            @separators.push(new_separator)

starter = new Starter()