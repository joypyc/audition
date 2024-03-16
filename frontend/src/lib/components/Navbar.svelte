<script>
    import {loggedUser} from '$lib/stores.js'
    import {getCookie} from '$lib/utils.js'
    import {logoutUrl} from '$lib/config.js'
    import {goto} from "$app/navigation";


    export let navLinks = []
    async function logout(){
        try{
            let res = await fetch(logoutUrl,{
                "credentials": "include",
                "method": "POST",
                "headers": {
                    "X-CSRFToken": getCookie('csrftoken')
                }
            })
            loggedUser.set(null)
            goto('/login')
        } catch (e){
            console.log(e)
            loggedUser.set(null)
            goto('/login')
        }
        
    }
</script>
<nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">AudiVentory</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" href="/inventory/list">Product</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/">User Management</a>
          </li>
        </ul>
        <form on:submit|preventDefault={logout}>
            <button class="btn btn-outline-success me-2" type="submit">Log out</button>
        </form>
      </div>
    </div>
</nav>