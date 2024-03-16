<script>
    import {loggedUser} from '$lib/stores.js'
    import {onMount} from 'svelte';
    import {goto} from '$app/navigation';
    import {csrfToken} from '$lib/stores';
    import {checkAuthUrl} from '$lib/config'
    import Navbar from '$lib/components/Navbar.svelte'
    let firstName = '';
    onMount( async()=>{
        let res = await fetch(checkAuthUrl,{
            "credentials": "include"
        })
        if (res.ok){
            let userData = await res.json()
            loggedUser.set({
                "id": userData['user']['id'],
                "firstName": userData['user']['first_name']
            })
            goto('/')
        } else {
            goto('/login')
        }
    })

</script>
<Navbar/>
<div class='container'>
<slot/>
</div>