<script>
    import {loggedUser} from '$lib/stores'
    import {onMount} from 'svelte';
    let firstName
    onMount(()=>{
        if ($loggedUser) firstName = $loggedUser['firstName']
    })
    
    let navigationCards = [
        {
            "title": "Products",
            "description": "View and manage list of products in the system",
            "list": '/inventory/list',
            "create": '/inventory/add',
            "add": true,
            "view": true,
        }
    ]
</script>

<h1>
    Welcome{#if firstName}, {firstName} {/if}
</h1>

<div class='row'>
    {#each navigationCards as card}
    <div class='col'>
        <div class="card" style="width: 18rem;">
            <div class="card-body">
              <h5 class="card-title">{card.title}</h5>
              <p class="card-text">{card.description}</p>
              {#if card.view}
              <a href="{card.list}" class="btn btn-primary">View</a>
              {/if}
              {#if card.add}
              <a href="{card.create}" class="btn btn-primary">Add</a>
              {/if}
            </div>
          </div>
    </div>
    {/each}
</div>