<script lang="ts">
	import type { FlowModule } from '$lib/gen'

	import FlowCardHeader from './FlowCardHeader.svelte'
	export let title: string | undefined = undefined
	export let flowModule: FlowModule | undefined = undefined
	export let noEditor: boolean
</script>

<div class="flex flex-col h-full">
	{#if !noEditor}
		<div>
			<FlowCardHeader on:reload {title} bind:flowModule>
				<slot name="header" />
			</FlowCardHeader>
		</div>
	{/if}

	<div class="min-h-0 flex-grow">
		<slot />
	</div>
</div>
