

<script>
    let url = "";
    let depth = 1;
    let query = "";
    let responseMsg = "";
    let responseClass=""
    let loading=false
    async function sendPost() {
        responseMsg=""
        const data = { url, depth, query };
        loading=true
        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                let responseData= await response.json()
                responseMsg = responseData.result;
                responseClass="success"
            } else {
                responseMsg = "Error during the search execution";
                responseClass="error"
            }
        } catch (error) {
            responseMsg = "Error during the search execution";
            responseClass="error"
        }
        loading=false
    }
</script>


<h1>Search an info in a web page</h1>

<div>
    <label for="url">URL</label>
    <input bind:value={url} placeholder="https://example.com">
    <label for="depth">Depth</label>
    <input bind:value={depth} placeholder="1">
    <label for="query">Query</label>
    <input bind:value={query} placeholder="info to search">
    <button on:click={sendPost}>Search</button>
</div>

{#if loading}
    <div id=loading></div>
{/if}
{#if responseMsg}
    <div class={responseClass}>{responseMsg}</div>
{/if}