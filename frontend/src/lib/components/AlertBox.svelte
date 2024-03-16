<script>
    export let message;
    export let mode='danger';
</script>

<div class="alert alert-{mode}" role="alert">
    {message}
</div>