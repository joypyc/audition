<script>
    import {onMount} from 'svelte';
    import {goto} from '$app/navigation'
    export let id='';
    export let name='';
    export let img='';
    export let supplier_id;
    export let category_id;
    export let price='';
    export let quantity=''
    export let supplier = {}; 
    export let category = {}; 
    export let serverSubmit;
    export let formDisabled = false


    let uploadedFile
    let fileInput
    let imageInput
    let container
    let placeholder
    let showImage = false;
    let formData = {}
    let formElement;

    onMount(()=>{
        supplier_id = String(supplier_id)
        category_id = String(category_id)
        if (img){
            // imageInput.src = img
            showImage = true
            
        }
    })
    function onUpload() {
        const file = fileInput.files[0];
        if (file) {
            showImage = true;

            const reader = new FileReader();
            reader.addEventListener("load", function () {
                imageInput.setAttribute("src", reader.result);
            });
            reader.readAsDataURL(file);
            uploadedFile = file
            return;
        } 
        showImage = false; 
    }
    function onSubmit(e){
            let fData = new FormData(formElement)
            serverSubmit(fData)
            let next_action = e.submitter.name
            if (next_action == 'save_exit'){
                goto('/inventory/list')
            }

    }
</script>

<form on:submit|preventDefault={onSubmit} id='productForm' enctype="multipart/form-data" bind:this={formElement}>
    <div class="mb-3">
        
        <h3> 
            {#if id}
                #{id} 
            {:else}
                Add Product
            {/if}
        </h3>
    </div>
    <div bind:this={container}>
        {#if showImage}
            <img bind:this={imageInput} src={img} alt="Preview" height=200 width=auto/>
        {:else}
            <span bind:this={placeholder}>Image Preview</span>
        {/if}
    </div>  
    <div class="form-group row mb-3">
        <input
            id='image'
            name='image'
            class='form-control'
            bind:this={fileInput}
            on:change={onUpload}
            type="file"
        />
    </div>
      
    <div class="row mb-3">
        <div class='col-md-2'>
        <label for="id" class="form-label">ID</label>
        </div>
        <div class='col'>
        <input type="text" class="form-control" id="id" name="id" aria-describedby="Record ID" bind:value={id} readonly>
        </div>
    </div>
    <div class="row mb-3">
        <div class='col-md-2'>
        <label for="name" class="form-label">Name</label>
        </div>
        <div class='col'>
        <input type="text" class="form-control" id="name" aria-describedby="Name" name="name" bind:value={name} disabled={formDisabled} required>
    </div>
    </div>
    <div class="row mb-3">
        <div class='col-md-2'>
        <label for="supplier" class="form-label">Supplier</label>
    </div>
    <div class='col'>
        <select class="form-select" disabled={formDisabled} name='product_supplier' id='product_supplier' bind:value={supplier_id}>
            <option disabled>Supplier</option>
            {#each Object.entries(supplier) as [key, val]}
                <option value="{key}">{val}</option>
            {/each}
        </select>
    </div>
    </div>
    <div class="row mb-3">
        <div class='col-md-2'>
        <label for="category" class="form-label">Category</label>
    </div>
    <div class='col'>
        <select class="form-select" disabled={formDisabled} name='product_category' id='product_category' bind:value={category_id}>
            <option disabled>Category</option>
            {#each Object.entries(category) as [key, val]}
                <option  value="{key}">{val}</option>
            {/each}
        </select>
    </div>
    </div>
    <div class="row mb-3">
        <div class='col-md-2'>
        <label for="price" class="form-label">Price</label>
    </div>
    <div class='col'>
        <input type="number" class="form-control" id="price" aria-describedby="Price" name='price' bind:value={price}  step="0.01" disabled={formDisabled}>
    </div>
    </div>
    <div class="row mb-3">
        <div class='col-md-2'>
        <label for="quantity" class="form-label">Quantity</label>
    </div>
    <div class='col'>
        <input type="number" class="form-control" id="quantity" name='quantity' aria-describedby="Quantity" bind:value={quantity} disabled={formDisabled}>
    </div>
    </div>
    
    <button type="submit" class="btn btn-primary" disabled={formDisabled} name='save'>Save</button>
    <button type="submit" class="btn btn-primary" disabled={formDisabled} name='save_exit'>Save and Exit</button>
  </form>