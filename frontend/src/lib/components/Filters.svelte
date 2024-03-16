<script>
    import {onMount} from 'svelte';
    import MultiSelect from 'svelte-multiselect'
    export let id;
    export let label;
    export let options;
    export let selectionStore;
    let selected = []

    function setSelection(selected){
        let currentSelection = $selectionStore
        if (id in currentSelection){
            currentSelection[id] = selected
        } else {
            currentSelection[id] = selected
        }
        selectionStore.set(currentSelection)
    }
    $: setSelection(selected)
</script>


<label for={label}>
    <strong>{label}</strong>
</label>

<MultiSelect bind:selected {id} {options}/>