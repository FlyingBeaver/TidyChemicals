tree = {
    cas:
        equals:
            verbose: 'equals'
            widget: 'numeral_input_cas'
        verbose: 'CAS RN'
    comment:
        ends_with:
            verbose: 'ends with'
            widget: 'text_input'
        exact_match:
            verbose: 'exact match'
            widget: 'text_input'
        includes:
            verbose: 'includes'
            widget: 'text_input'
        starts_with:
            verbose: 'starts with'
            widget: 'text_input'
        verbose: 'Comment'
    molar_mass:
        equals:
            verbose: 'equals'
            widget: 'numeral_input'
        equals_with_epsilon:
            verbose: 'equals with epsilon'
            widget: 'special_numeral_input'
        in_interval_between:
            verbose: 'in interval between'
            widget: 'two_numeral_inputs'
        less_than:
            verbose: 'less than'
            widget: 'numeral_input'
        more_than:
            verbose: 'more than'
            widget: 'numeral_input'
        verbose: 'Molar mass'
    molecular_formula:
        exact_match:
            verbose: 'exact match'
            widget: 'formula_text_input'
        includes:
            verbose: 'includes'
            widget: 'formula_text_input'
        verbose: 'Molecular formula'
    name:
        ends_with:
            verbose: 'ends with'
            widget: 'text_input_with_format'
        exact_match:
            verbose: 'exact match'
            widget: 'text_input_with_format'
        includes:
            verbose: 'includes'
            widget: 'text_input_with_format'
        starts_with:
            verbose: 'starts with'
            widget: 'text_input_with_format'
        verbose: 'Name'
    quantity_with_unit:
        equals:
            verbose: 'equals'
            widget: 'numeral_and_unit'
        equals_with_epsilon:
            verbose: 'in interval around'
            widget: 'numeral_epsilon_unit'
        in_interval_between:
            verbose: 'in interval between'
            widget: 'two_numerals_and_unit'
        less_than:
            verbose: 'less than'
            widget: 'numeral_and_unit'
        more_than:
            verbose: 'more than'
            widget: 'numeral_and_unit'
        verbose: 'Quantity'
    storage_place:
        choose_from_list:
            verbose: 'choice from the list'
            widget: 'storage_place_input'
        verbose: 'Storage place'
    structure:
        exact_match:
            verbose: 'exact match'
            widget: 'jsme_input'
        substructure:
            verbose: 'substructure'
            widget: 'jsme_input'
        substructure_greedy:
            verbose: 'substructure (greedy)'
            widget: 'jsme_input'
        verbose: 'Structure'
    synonym:
        ends_with:
            verbose: 'ends with'
#           widget: 'text_input_with_format'
            widget: 'text_input'
        exact_match:
            verbose: 'exact match'
#           widget: 'text_input_with_format'
            widget: 'text_input'
        includes:
            verbose: 'includes'
#           widget: 'text_input_with_format'
            widget: 'text_input'
        starts_with:
            verbose: 'starts with'
#           widget: 'text_input_with_format'
            widget: 'text_input'
        verbose: 'Synonym'
    when_created:
        date_before:
            verbose: 'date before'
            widget: 'date_input'
        date_from:
            verbose: 'date from'
            widget: 'date_input'
        date_range:
            verbose: 'date range'
            widget: 'date_range_input'
        verbose: 'Creation date'
    when_updated:
        date_before:
            verbose: 'date before'
            widget: 'date_input'
        date_from:
            verbose: 'date from'
            widget: 'date_input'
        date_range:
            verbose: 'date range'
            widget: 'date_range_input'
        verbose: 'Last update date'
    who_created:
        choose_profile_from_list:
            verbose: 'choice of profile from the list'
            widget: 'select_profile_from_list'
        type:
            verbose: 'text input'
            widget: 'text_input'
        type_with_prompts:
            verbose: 'prompted text input'
            widget: 'prompted_text_input'
        verbose: 'Created by'
    who_updated:
        choose_profile_from_list:
            verbose: 'choice of profile from the list'
            widget: 'select_profile_from_list'
        type:
            verbose: 'text input'
            widget: 'text_input'
        type_with_prompts:
            verbose: 'prompted text input'
            widget: 'prompted_text_input'
        verbose: 'Updated by'
}

SELECT_INNER_HTML = '''<option value="" selected>Choose search option</option>
<option value="cas">CAS RN</option>
<option value="comment">Comment</option>
<option value="molar_mass">Molar mass</option>
<option value="molecular_formula">Molecular formula</option>
<option value="name">Name</option>
<option value="quantity_with_unit">Quantity</option>
<option value="storage_place">Storage place</option>
<option value="structure">Structure</option>
<option value="synonym">Synonym</option>
<option value="when_created">Creation date</option>
<option value="when_updated">Last update date</option>
<option value="who_created">Created by</option>
<option value="who_updated">Updated by</option>'''

CONNECTOR_SELECT_INNER_HTML = '''<option value="" selected>AND / NOT / AND NOT</option>
<option value="and">And</option>
<option value="or">Or</option>
<option value="and_not">And not</option>'''


class Hierarchy
    # Singleton, that stores hierarchy
    @instance: undefined
    @counter: 0

    constructor: (hierarchy_object) ->
        if Hierarchy.counter == 0
            @hierarchy_object = hierarchy_object
            Hierarchy.counter = 1
            Hierarchy.instance = @
        else
            return Hierarchy.instance

    make_term_menu_object: () ->
# Makes object for "search option" menu
# (left column).
# Result is like {name: verbose}
        result = {}
        for key of @hierarchy_object
            result[key] = @hierarchy_object[key].verbose
        return result

    make_operators_menu_object: (term) ->
# Makes object for "operator" menu
# (central column)
# Result is like {name: verbose}
        result = {}
        for key of @hierarchy_object[term]
            if key == "verbose" or key == "name"
                continue
            else
                result[key] = @hierarchy_object[term][key].verbose
        return result

    @what_widget: (term_name, operator_name) ->
        if `term_name in Hierarchy.instance.hierarchy_object`
            if `operator_name in Hierarchy.instance.hierarchy_object[term_name]`
                return Hierarchy.instance.hierarchy_object[term_name][operator_name].widget
            else throw("term_name IS in @hierarchy_object, BUT " +
                "operator_name not in @hierarchy_object[term_name][operator_name]")
        else throw("term_name is not in @hierarchy_object")


span_not_implemented = document.createElement("span")
#span_not_implemented.outerHTML = '<span class="inactive-field">'+
#                                 'Not implemented yet</span>'
span_not_implemented.classList.add("inactive-field")
span_not_implemented.textContent = 'Not implemented yet'


class Widget
    name = ""
    values_p_content = null
    appendix_content = null
    values_p_functions = {}
    appendix_functions = {}
    @instances = {}
    @not_implemented = span_not_implemented
    constructor: (name) ->
        @p_value_content = null
        @appendix_content = null
        @p_value_functions = {}
        @appendix_functions = {}
        @name = name
        Widget.instances[name] = @


ti = document.createElement("input")
ti.type = 'text'
ti.classList.add('simple_text_value')
ti.name = 'text_value'
#ti.outerHTML = '<input type="text" class="simple_text_value" name="text_value">'
text_input = new Widget("text_input")
text_input.p_value_content = ti



hierarchy = new Hierarchy(tree)



#Row state codes:
ACTIVE = 1
INACTIVE = 2
FIRED = 3
EXPANDED = 4
NO_STATE_YET = 0


class Container
    instance: undefined
    length: 0
    subforms_array: []
    keys_array: []
    form_node: undefined

    constructor: () ->
        if Container.instance
            return Container.instance
        else
            Container.instance = @
            @form_node = document.querySelector('form')
            Object.defineProperty @, "length",
                get: ->
                    return @form_node.querySelectorAll('div.row').length
            @subforms_array = [new Subform(), new ButtonBox()]
            @keys_array = [@subforms_array[0].key
                @subforms_array[1].key]
            return @

    calc_bro_index: (index) ->
        if typeof index != "number"
            throw new TypeError("Wrong 'index' type: #{typeof index}")
        else if index % 1 != 0 or index > Container.instance.length or index < 0
            throw new Error("Wrong value of 'index': #{index}")
        else if index % 2 == 0 and index != Container.instance.length - 2
            return index + 1
        else
            return index - 1

    turn_deletion_mode_ON: () =>
        rows = @subforms_array.slice()
        if rows[rows.length - 1].key == "button_box"
            rows.pop()
        else
            throw Error("Last row isn't button_box")
        for row in rows
            row.node.addEventListener("mouseenter", @event_processor)
            row.node.addEventListener("mouseleave", @event_processor)
            row.node.addEventListener("click", @event_processor)
        @form_node.classList.add("deletion_mode")
        return null

    turn_deletion_mode_OFF: () =>
        rows = @subforms_array.slice()
        if rows[rows.length - 1].key == "button_box"
            rows.pop()
        else
            throw Error("Last row isn't button_box")
        for row in rows
            row.switch_state(ACTIVE)
            row.node.removeEventListener("mouseenter", @event_processor)
            row.node.removeEventListener("mouseleave", @event_processor)
            row.node.removeEventListener("click", @event_processor)
        @form_node.classList.remove("deletion_mode")

    event_processor: (event) =>
        event_target = event.target
        # сначала нужно найти подходящий Tagret
        while "row" not in event_target.classList
            event_target = event_target.parentNode
            if event_target.nodeName == "FORM"
                throw Error("FORM element achieved")
        target_index = @keys_array.indexOf(event_target.id)
        #        while target_index == -1
        #            event_target = event_target.parentNode
        #            target_index = @keys_array.indexOf(event_target.id)
        bro_index = @calc_bro_index(target_index)
        if event.type == "mouseenter"
            @subforms_array[bro_index].switch_state(FIRED)
        else if event.type == "mouseleave"
            @subforms_array[bro_index].switch_state(INACTIVE)
        else if event.type == "click"
            @delete_two_rows(target_index, bro_index)
            #@delete_row(bro_index)
            @update_connectors()
#            # здесь
#            @check_if_forced_state_change_needed()
#            # выше
        else
            throw new Error("unknown event type")

#    #<здесь>
#    check_if_forced_state_change_needed: () ->
#        if 'deletion_mode' in @form_node.classList and
#          @form_node.querySelectorAll(".row").length < 4
#            @turn_deletion_mode_OFF
#        return null
#    #</здесь>

    delete_two_rows: (target_index, bro_index) ->
        if target_index < bro_index
            less_index = target_index
            @form_node.children[bro_index].remove()
            @form_node.children[target_index].remove()
        else
            less_index = bro_index
            @form_node.children[target_index].remove()
            @form_node.children[bro_index].remove()
        @subforms_array.splice(less_index, 2)
        @keys_array.splice(less_index, 2)

#    @delete_elem_from_arr_with_idx: (array_, index_) ->
#        length_ = array_.length
#        return array_.slice(0, index_)
#            .concat(array_.slice(index_ + 1, length_))


    update_connectors: () ->
        for row_number in [1..@subforms_array.length - 1]
            if @subforms_array[row_number] instanceof Connector
                if @subforms_array[row_number - 1] instanceof Subform and
                  @subforms_array[row_number + 1] instanceof Subform
                    key_has_to_be_equal = @subforms_array[row_number - 1]
                    key_has_to_be_equal += "_plus_"
                    key_has_to_be_equal += @subforms_array[row_number + 1]
                    if not @subforms_array[row_number].key == key_has_to_be_equal
                        @subforms_array[row_number].node.id = key_has_to_be_equal
                else
                    throw new Error("Connector is not between two subforms")
            else
                continue

    add_rows_pair: () =>
        butbox = document.getElementById("buttons_box")
        previous_subform_id = butbox.previousElementSibling.id
        new_subform = new Subform()
        butbox.before(new_subform.node)
        new_connector = new Connector(previous_subform_id, new_subform.key)
        new_subform.node.before(new_connector.node)
        @keys_array = Container.add_to_array_before_last(
            @keys_array, new_connector.key
        )
        @subforms_array = Container.add_to_array_before_last(
            @subforms_array, new_connector
        )
        @keys_array = Container.add_to_array_before_last(
            @keys_array, new_subform.key
        )
        @subforms_array = Container.add_to_array_before_last(
            @subforms_array, new_subform
        )

    @add_to_array_before_last: (array_to_append, element_to_add) ->
        return (array_to_append.slice(0, -1)).concat(element_to_add, array_to_append.slice(-1))


class Row
    valid_states = []
    node = undefined
    key = ""
    state_code = NO_STATE_YET
    switch_state = undefined

    constructor: () ->
        @state_code = ACTIVE
        @valid_states = []

    @create_node: ({element = 'div'
        class_name = ''
        id_name = ''
        parameters = {}
        inner_html = ''
        daughters = []}) ->
        new_node = document.createElement(element)
        if class_name != '' and typeof class_name == "string"
            for class_ in class_name.split(' ')
                new_node.classList.add(class_)
        if id_name != '' and typeof id_name == "string"
            new_node.id = id_name
        if JSON.stringify(parameters) != "{}"
            for par, value of parameters
                new_node[par] = value
        if typeof inner_html == "string" and inner_html != ""
            new_node.innerHTML = inner_html
        if JSON.stringify(daughters) != "[]"
            for node in daughters
                new_node.append(node)
        return new_node

    has_such_class: (class_name) ->
        return class_name in @classes_list

    add_class: (class_name) ->
        if not @has_such_class(class_name)
            @node.classList.add(class_name)
        else
            throw new Error("This class already added: #{class_name}")

    delete_class: (class_name) ->
        if @has_such_class(class_name)
            @node.classList.remove(class_name)
        else
            throw new Error("Node don't have this class")

    validate_state: (state_code) ->
        if typeof @state_code != 'number'
            throw new TypeError("instance state_code " +
                "has wrong type: #{typeof @state_code}")
        if typeof state_code != "number"
            throw new TypeError("state_code has wrong type: #{typeof state_code}")
        else if state_code in @valid_states
            return true
        else
            console.log "valid_states: \n#{@valid_states}"
            throw new Error("State with this code is not " +
                "available. State code: #{state_code}")


class Subform extends Row
    @counter = 0

    constructor: () ->
        super()
        @key = "subform#{Subform.counter}"
        if Subform.counter == 0
            @node = document.querySelector('div#' + @key)
            select = @node.querySelector("select")
            select.addEventListener("change", @term_listener)
            p_term = select.parentNode
            p_operator = @node.querySelector('p.operator_box')
            p_value = @node.querySelector('p.value_box')
        else
            key_plus_term = @key + "_term"
            select = Subform.create_node({
                element: "select"
                parameters: `{required: "required",
                             name: key_plus_term}`
                inner_html: SELECT_INNER_HTML
            })
            p_term = Subform.create_node({
                element: "p"
                class_name: "column"
                daughters: [select]
            })
            p_operator = Subform.create_node({
                element: "p"
                class_name: "operator_box column"
                inner_html: '<span class="inactive-field">Operator</span>'
            })
            p_value = Subform.create_node({
                element: "p"
                class_name: "value_box column"
                inner_html: '<span class="inactive-field">Value</span>'
            })
            @node = Subform.create_node({
                element: "div"
                class_name: "row"
                id_name: @key
                daughters: [p_term
                    p_operator
                    p_value]
            })
        @p_term = p_term
        @p_operator = p_operator
        @p_value = p_value
        @select = select
        @select.addEventListener("change", @term_listener)
        Object.defineProperty @, "classes_list",
            get: ->
                return new Array(@node.classList)
        Object.defineProperty @, "subform_no",
            get: ->
                return @node.id
        @valid_states = [ACTIVE
            INACTIVE
            FIRED
            EXPANDED]
        @state_code = 1
        Subform.counter += 1
        return @

    switch_state: (new_state_code) ->
        if new_state_code == @state_code
            return null
        @validate_state(new_state_code)
        # Back to ACTIVE
        if @state_code == INACTIVE
            for element in @node.querySelectorAll("[disabled]")
                element.removeAttribute("disabled")
        else if @state_code == FIRED
            @node.classList.remove("fired")
        else if @state_code == EXPANDED
            @node.querySelector("div.appendix").remove()

        # From ACTIVE to new state
        if new_state_code == INACTIVE
            for element in @node.querySelectorAll("select, input[type='text']")
                element.setAttribute("disabled", "disabled")
        else if new_state_code == FIRED
            @node.classList.add("fired")
        else if new_state_code == EXPANDED
            appendix = Subform.create_node(`{element: "div",
                class_name: "appendix"}`)
            @node.append(appendix)
        @state_code = new_state_code

    term_listener: (event) =>
        what_chosen = event.target.value
        operators_menu_object = hierarchy.make_operators_menu_object(what_chosen)
        @update_operator(operators_menu_object)

    update_operator: (operators_menu_object)=>
        operators_menu_code = "<option value='' selected>Choose operator</option>"
        for key, value of operators_menu_object
            operators_menu_code += "<option value='#{key}'>#{value}</option>"
        new_select = Subform.create_node(`{
            element: "select",
                parameters: {name: key + "_operator",
                required: "required"},
            inner_html: operators_menu_code,
        }`)
        @p_operator.children[0].replaceWith(new_select)
        new_select.addEventListener("change", @operator_listener)

    operator_listener: (event) =>
        chosen_operator = event.target.value
        chosen_term = @p_term.children[0].value
        selected_widget_name = Hierarchy.what_widget(chosen_term,
            chosen_operator)
        all_widget_names = Object.keys(Widget.instances)
        if selected_widget_name in all_widget_names
            the_widget = Widget.instances[selected_widget_name]
            @update_widget(the_widget)
        else
            @update_widget("not_implemented")

    update_widget: (widget) =>
        if widget == "not_implemented"
            @p_value.children[0].replaceWith(Widget.not_implemented)
        else if widget instanceof Widget
            @p_value.children[0].replaceWith(widget.p_value_content)
        else
            throw new TypeError("Wrong widget type")


class Connector extends Row
    @number_up: 0
    @number_down: 0

    constructor: (up, down) ->
        super()
        @valid_states = [ACTIVE
            INACTIVE
            FIRED]
        @number_up = up
        @number_down = down
        key = "#{up}_plus_#{down}"
        select = Connector.create_node(`{
            element: "select",
                parameters: {name: key,
                required: "required"},
            inner_html: CONNECTOR_SELECT_INNER_HTML,
        }`)
        div_container = Connector.create_node({
            element: "div"
            class_name: "operator_between_box"
            daughters: [select]
        })
        @node = Connector.create_node({
            element: "div"
            class_name: "row"
            id_name: key
            daughters: [div_container]
        })
        Object.defineProperty @, "key",
            get: ->
                return @node.getAttribute("id")
            set: (value) ->
                if @node.getAttribute("id") != value
                    @node.removeAttribute("id")
                    @node.setAttribute("id", value)

    switch_state: (new_state_code) ->
        if new_state_code == @state_code
            return null
        @validate_state(new_state_code)
        # Back to ACTIVE
        if @state_code == INACTIVE
            for element in @node.querySelectorAll("[disabled]")
                element.removeAttribute("disabled")
            @state_code = ACTIVE
        else if @state_code == FIRED
            @node.classList.remove("fired")
            @state_code = ACTIVE

        # From ACTIVE to new state
        if new_state_code == INACTIVE
            for element in @node.querySelectorAll("select, input[type='text']")
                element.setAttribute("disabled", "disabled")
            @state_code = INACTIVE
        else if new_state_code == FIRED
            @node.classList.add("fired")
            @state_code = FIRED

    write_numbers_to_dom: () ->
        @key = "#{@number_up}_plus_#{number_down}"


class ButtonBox extends Row
    # Singleton
    @instance: null
    key: "button_box"
    button_CREATE: null
    button_DELETE: null
    button_DELETE_shelter: null

    constructor: () ->
        if ButtonBox.instance
            return ButtonBox.instance
        else
            super()
            # THREE_BUTTONS_INACTIVE -- when molecular
            # editor open and several subforms are on page
            @valid_states = [ACTIVE
                INACTIVE]
            @key = "button_box"
            @node = document.getElementById("buttons_box")
            @button_CREATE = @node.querySelector("#more_conditions")
            @button_CREATE.addEventListener("click", @when_CREATE_clicked)
            @button_DELETE = @node.querySelector("#delete_button")
            @button_DELETE.addEventListener('click',
                Container.instance.turn_deletion_mode_ON
            )
            @button_EXIT = @node.querySelector("#exit_from_deletion")
            @button_EXIT.addEventListener('click',
                Container.instance.turn_deletion_mode_OFF
            )
            ButtonBox.instance = @
            return @

    switch_state: (new_state_code) ->
        @validate_state(new_state_code)
        if @state_code == INACTIVE and new_state_code == ACTIVE
            for element in @node.querySelectorAll("[disabled]")
                if element.id != 'more_conditions_disabled'
                    element.removeAttribute("disabled")
            @state_code = new_state_code
        else if @state_code == ACTIVE and new_state_code == INACTIVE
            for element in @node.querySelectorAll("button")
                if element.id != 'more_conditions_disabled'
                    element.setAttribute("disabled", "disabled")
            @state_code = new_state_code

    when_CREATE_clicked: (event) =>
        Container.instance.add_rows_pair()
        return null



the_container = new Container()

#class Tester
#    constructor: () ->
#        click = new Event("click")
#        document.querySelector("#more_conditions").dispatchEvent(click)
#        document.querySelector("#more_conditions").dispatchEvent(click)
#        document.querySelector("#delete_button").dispatchEvent(click)
#        document.querySelector("#subform2").dispatchEvent(click)
#
#class Tester2
#    constructor: () ->
#        click = new Event("click")
#        document.querySelector("#more_conditions").dispatchEvent(click)
#        document.querySelector("#more_conditions").dispatchEvent(click)
#        document.querySelector("#delete_button").dispatchEvent(click)
#
#t = new Tester2()
