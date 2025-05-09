<script lang="ts">
	import { OauthService, type ResourceType } from '$lib/gen'
	import { workspaceStore } from '$lib/stores'
	import { base } from '$lib/base'
	import { emptySchema, emptyString } from '$lib/utils'
	import SchemaForm from './SchemaForm.svelte'
	import type SimpleEditor from './SimpleEditor.svelte'
	import Toggle from './Toggle.svelte'
	import TestConnection from './TestConnection.svelte'
	import SupabaseIcon from './icons/SupabaseIcon.svelte'
	import Popover from './meltComponents/Popover.svelte'
	import Button from './common/button/Button.svelte'
	import { Loader2 } from 'lucide-svelte'

	export let resourceType: string
	export let resourceTypeInfo: ResourceType | undefined
	export let args: Record<string, any> | any = {}
	export let linkedSecret: string | undefined = undefined
	export let isValid = true
	export let linkedSecretCandidates: string[] | undefined = undefined

	let schema = emptySchema()
	let notFound = false

	let supabaseWizard = false

	async function isSupabaseAvailable() {
		try {
			supabaseWizard =
				((await OauthService.listOauthConnects()) ?? {})['supabase_wizard'] != undefined
		} catch (error) {}
	}
	async function loadSchema() {
		if (!resourceTypeInfo) return
		rawCode = '{}'
		viewJsonSchema = false
		try {
			schema = resourceTypeInfo.schema as any

			schema.order = schema.order ?? Object.keys(schema.properties).sort()

			notFound = false
		} catch (e) {
			notFound = true
		}
	}
	$: $workspaceStore && loadSchema()

	$: notFound && rawCode && parseJson()

	function parseJson() {
		try {
			args = JSON.parse(rawCode)
			error = ''
			isValid = true
		} catch (e) {
			isValid = false
			error = e.message
		}
	}
	let error = ''
	let rawCode = ''
	let viewJsonSchema = false

	$: rawCode && parseJson()

	$: textFileContent && parseTextFileContent()

	function switchTab(asJson: boolean) {
		viewJsonSchema = asJson
		if (asJson) {
			rawCode = JSON.stringify(args, null, 2)
		} else {
			parseJson()
			if (resourceTypeInfo?.format_extension) {
				textFileContent = args.content
			}
		}
	}

	$: resourceType == 'postgresql' && isSupabaseAvailable()

	let connectionString = ''
	let validConnectionString = true
	function parseConnectionString(close: (_: any) => void) {
		const regex =
			/postgres(?:ql)?:\/\/(?<user>[^:@]+)(?::(?<password>[^@]+))?@(?<host>[^:\/?]+)(?::(?<port>\d+))?\/(?<dbname>[^\?]+)?(?:\?.*sslmode=(?<sslmode>[^&]+))?/
		const match = connectionString.match(regex)
		if (match) {
			validConnectionString = true
			const { user, password, host, port, dbname, sslmode } = match.groups!
			rawCode = JSON.stringify(
				{
					...args,
					user,
					password: password || args?.password,
					host,
					port: (port ? Number(port) : undefined) || args?.port,
					dbname: dbname || args?.dbname,
					sslmode: sslmode || args?.sslmode
				},
				null,
				2
			)
			rawCodeEditor?.setCode(rawCode)
			close(null)
		} else {
			validConnectionString = false
		}
	}

	let rawCodeEditor: SimpleEditor | undefined = undefined
	let textFileContent: string

	function parseTextFileContent() {
		args = {
			content: textFileContent
		}
	}
</script>

{#if !notFound}
	<div class="w-full flex gap-4 flex-row-reverse items-center">
		<Toggle
			on:change={(e) => switchTab(e.detail)}
			options={{
				right: 'As JSON'
			}}
		/>
		<TestConnection {resourceType} {args} />
		{#if resourceType == 'postgresql'}
			<Popover
				floatingConfig={{
					placement: 'bottom'
				}}
			>
				<svelte:fragment slot="trigger">
					<Button
						spacingSize="sm"
						size="xs"
						btnClasses="h-8"
						color="light"
						variant="border"
						nonCaptureEvent
					>
						From connection string
					</Button>
				</svelte:fragment>
				<svelte:fragment slot="content" let:close>
					<div class="block text-primary p-4">
						<div class="w-[550px] flex flex-col items-start gap-1">
							<div class="flex flex-row gap-1 w-full">
								<input
									type="text"
									bind:value={connectionString}
									placeholder="postgres://user:password@host:5432/dbname?sslmode=disable"
								/>
								<Button
									size="xs"
									color="blue"
									buttonType="button"
									on:click={() => {
										parseConnectionString(close)
									}}
									disabled={connectionString.length <= 0}
								>
									Apply
								</Button>
							</div>
							{#if !validConnectionString}
								<p class="text-red-500 text-xs">Could not parse connection string</p>
							{/if}
						</div>
					</div>
				</svelte:fragment>
			</Popover>
		{/if}
		{#if resourceType == 'postgresql' && supabaseWizard}
			<a
				target="_blank"
				href="{base}/api/oauth/connect/supabase_wizard"
				class="border rounded-lg flex flex-row gap-2 items-center text-xs px-3 py-1.5 h-8 bg-[#F1F3F5] hover:bg-[#E6E8EB] dark:bg-[#1C1C1C] dark:hover:bg-black"
			>
				<SupabaseIcon height="16px" width="16px" />
				<div class="text-[#11181C] dark:text-[#EDEDED] font-semibold">Connect Supabase</div>
			</a>
		{/if}
	</div>
{:else}
	<p class="italic text-tertiary text-xs mb-4"
		>No corresponding resource type found in your workspace for {resourceType}. Define the value in
		JSON directly</p
	>
{/if}
{#if notFound || viewJsonSchema}
	{#if !emptyString(error)}<span class="text-red-400 text-xs mb-1 flex flex-row-reverse"
			>{error}</span
		>{:else}<div class="py-2" />{/if}
	<div class="h-full w-full border p-1 rounded">
		{#await import('$lib/components/SimpleEditor.svelte')}
			<Loader2 class="animate-spin" />
		{:then Module}
			<Module.default
				bind:this={rawCodeEditor}
				autoHeight
				lang="json"
				bind:code={rawCode}
				fixedOverflowWidgets={false}
			/>
		{/await}
	</div>
{:else if resourceTypeInfo?.format_extension}
	<h5 class="mt-4 inline-flex items-center gap-4">
		File content ({resourceTypeInfo.format_extension})
	</h5>
	<div class="py-2" />
	<div class="h-full w-full border p-1 rounded">
		{#await import('$lib/components/SimpleEditor.svelte')}
			<Loader2 class="animate-spin" />
		{:then Module}
			<Module.default
				bind:this={rawCodeEditor}
				autoHeight
				lang={resourceTypeInfo.format_extension}
				bind:code={textFileContent}
				fixedOverflowWidgets={false}
			/>
		{/await}
	</div>
{:else}
	<SchemaForm
		onlyMaskPassword
		noDelete
		{linkedSecretCandidates}
		bind:linkedSecret
		isValid
		{schema}
		bind:args
	/>
{/if}
