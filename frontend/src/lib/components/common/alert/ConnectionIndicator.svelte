<script context="module" lang="ts">
	export type ConnectionInfo = {
		connected: boolean
		message?: string
	}
</script>

<script lang="ts">
	import Popover from '$lib/components/Popover.svelte'
	import { Circle } from 'lucide-svelte'

	export let connectionInfo: ConnectionInfo | undefined = undefined
</script>

{#if connectionInfo}
	<div class="center-center">
		{#if connectionInfo.connected}
			<Popover notClickable>
				<span class="h-4 w-4 center-center">
					<Circle class="text-green-600 relative inline-flex fill-current" size={12} />
				</span>

				<div slot="text"> {connectionInfo.message ?? ''} </div>
			</Popover>
		{:else}
			<Popover notClickable>
				<span class="h-4 w-4 center-center">
					<Circle class="text-red-600 animate-ping absolute inline-flex fill-current" size={12} />
					<Circle class="text-red-600 relative inline-flex fill-current" size={12} />
				</span>

				<div slot="text"> {connectionInfo.message ?? ''} </div>
			</Popover>
		{/if}
	</div>
{/if}
