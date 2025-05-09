<script context="module">
	let cssClassesLoaded = writable(false)
	let tailwindClassesLoaded = writable(false)

	import '@codingame/monaco-vscode-standalone-languages'
	import '@codingame/monaco-vscode-standalone-json-language-features'
	import '@codingame/monaco-vscode-standalone-css-language-features'
	import '@codingame/monaco-vscode-standalone-typescript-language-features'

	languages.typescript.javascriptDefaults.setCompilerOptions({
		target: languages.typescript.ScriptTarget.Latest,
		allowNonTsExtensions: true,
		noSemanticValidation: false,
		noLib: true,
		moduleResolution: languages.typescript.ModuleResolutionKind.NodeJs
	})
	languages.typescript.javascriptDefaults.setDiagnosticsOptions({
		noSemanticValidation: false,
		noSyntaxValidation: false,
		noSuggestionDiagnostics: false,
		diagnosticCodesToIgnore: [1108]
	})
	languages.json.jsonDefaults.setDiagnosticsOptions({
		validate: true,
		allowComments: false,
		schemas: [],
		enableSchemaRequest: true
	})
	languages.json.jsonDefaults.setModeConfiguration({
		documentRangeFormattingEdits: false,
		documentFormattingEdits: true,
		hovers: true,
		completionItems: true,
		documentSymbols: true,
		tokens: true,
		colors: true,
		foldingRanges: true,
		selectionRanges: true,
		diagnostics: true
	})
</script>

<script lang="ts">
	import { BROWSER } from 'esm-env'

	import { createHash, editorConfig, langToExt, updateOptions } from '$lib/editorUtils'
	import {
		editor as meditor,
		KeyCode,
		KeyMod,
		Uri as mUri,
		languages,
		type IRange,
		type IDisposable
	} from 'monaco-editor'

	import { allClasses } from './apps/editor/componentsPanel/cssUtils'

	import { createEventDispatcher, onDestroy, onMount } from 'svelte'

	import libStdContent from '$lib/es6.d.ts.txt?raw'
	import domContent from '$lib/dom.d.ts.txt?raw'
	import { initializeVscode } from './vscode'
	import EditorTheme from './EditorTheme.svelte'
	import { writable } from 'svelte/store'
	import { vimMode } from '$lib/stores'
	import { initVim } from './monaco_keybindings'
	import { buildWorkerDefinition } from '$lib/monaco_workers/build_workers'
	// import { createConfiguredEditor } from 'vscode/monaco'
	// import type { IStandaloneCodeEditor } from 'vscode/vscode/vs/editor/standalone/browser/standaloneCodeEditor'

	let divEl: HTMLDivElement | null = null
	let editor: meditor.IStandaloneCodeEditor
	let model: meditor.ITextModel

	export let lang: string
	export let code: string = ''
	export let hash: string = createHash()
	export let cmdEnterAction: (() => void) | undefined = undefined
	export let formatAction: (() => void) | undefined = undefined
	export let automaticLayout = true
	export let extraLib: string = ''
	export let placeholder: string = ''

	export let shouldBindKey: boolean = true
	export let autoHeight = false
	export let fixedOverflowWidgets = true
	export let small = false
	export let domLib = false
	export let autofocus = false
	export let allowVim = false
	export let tailwindClasses: string[] = []

	const dispatch = createEventDispatcher()

	const uri = `file:///${hash}.${langToExt(lang)}`

	buildWorkerDefinition()

	export function getCode(): string {
		return editor?.getValue() ?? ''
	}

	export function insertAtCursor(code: string): void {
		if (editor) {
			editor.trigger('keyboard', 'type', { text: code })
		}
	}

	export function setCode(ncode: string): void {
		code = ncode
		editor?.setValue(ncode)
	}

	let placeholderVisible = false
	function updatePlaceholderVisibility(value: string) {
		if (!value) {
			placeholderVisible = true
			return
		}
		placeholderVisible = value.trim() === ''
	}

	export function format() {
		if (editor) {
			code = getCode()
			editor.getAction('editor.action.formatDocument')?.run()
			if (formatAction) {
				formatAction()
				code = getCode()
			}
		}
	}

	export function focus() {
		editor?.focus()
	}

	export function getSelectedLines(): string | undefined {
		if (editor) {
			const selection = editor.getSelection()
			if (selection) {
				const range: IRange = {
					startLineNumber: selection.startLineNumber,
					startColumn: 1,
					endLineNumber: selection.endLineNumber + 1,
					endColumn: 1
				}
				return editor.getModel()?.getValueInRange(range)
			}
		}
	}

	export function onDidChangeCursorSelection(f: (e: meditor.ICursorSelectionChangedEvent) => void) {
		if (editor) {
			return editor.onDidChangeCursorSelection(f)
		}
	}

	export function show(): void {
		divEl?.classList.remove('hidden')
	}

	export function hide(): void {
		divEl?.classList.add('hidden')
	}

	let suggestion = ''
	export function setSuggestion(value: string): void {
		suggestion = value
	}

	let width = 0
	let initialized = false

	let disableTabCond: meditor.IContextKey<boolean> | undefined
	$: disableTabCond?.set(!code && !!suggestion)

	let statusDiv: Element | null = null

	let vimDisposable: IDisposable | undefined = undefined
	$: allowVim && editor && $vimMode && statusDiv && onVimMode()
	$: !$vimMode && vimDisposable && onVimDisable()

	function onVimDisable() {
		vimDisposable?.dispose()
	}

	function onVimMode() {
		if (editor && statusDiv) {
			vimDisposable = initVim(editor, statusDiv, () => {
				console.log('vim save not possible for simple editor')
			})
		}
	}

	async function loadMonaco() {
		await initializeVscode()
		initialized = true

		// if (lang === 'javascript') {
		// 	languages.typescript.javascriptDefaults.setCompilerOptions({
		// 		target: languages.typescript.ScriptTarget.Latest,
		// 		allowNonTsExtensions: true,
		// 		noSemanticValidation: false,
		// 		noLib: true,
		// 		moduleResolution: languages.typescript.ModuleResolutionKind.NodeJs
		// 	})
		// 	languages.typescript.javascriptDefaults.setDiagnosticsOptions({
		// 		noSemanticValidation: false,
		// 		noSyntaxValidation: false,
		// 		noSuggestionDiagnostics: false,
		// 		diagnosticCodesToIgnore: [1108]
		// 	})
		// } else if (lang === 'json') {
		// 	languages.json.jsonDefaults.setDiagnosticsOptions({
		// 		validate: true,
		// 		allowComments: false,
		// 		schemas: [],
		// 		enableSchemaRequest: true
		// 	})
		// }
		try {
			model = meditor.createModel(code, lang, mUri.parse(uri))
		} catch (err) {
			console.log('model already existed', err)
			const nmodel = meditor.getModel(mUri.parse(uri))
			if (!nmodel) {
				throw err
			}
			model = nmodel
		}
		model.updateOptions(updateOptions)
		// let widgets: HTMLElement | undefined =
		// 	document.getElementById('monaco-widgets-root') ?? undefined

		if (!divEl) {
			return
		}
		editor = meditor.create(divEl as HTMLDivElement, {
			...editorConfig(code, lang, automaticLayout, fixedOverflowWidgets),
			model,
			lineDecorationsWidth: 6,
			lineNumbersMinChars: 2,
			// overflowWidgetsDomNode: widgets,
			fontSize: small ? 12 : 14
		})

		let timeoutModel: NodeJS.Timeout | undefined = undefined
		editor.onDidChangeModelContent((event) => {
			suggestion = ''
			timeoutModel && clearTimeout(timeoutModel)
			timeoutModel = setTimeout(() => {
				code = getCode()
				dispatch('change', { code })
			}, 200)
		})

		editor.onDidFocusEditorText(() => {
			dispatch('focus')
			loadExtraLib()

			editor.addCommand(KeyMod.CtrlCmd | KeyCode.KeyS, function () {
				code = getCode()
				shouldBindKey && format && format()
			})

			disableTabCond = editor.createContextKey('disableTabCond', !code)
			editor.addCommand(KeyCode.Tab, function () {}, 'disableTabCond')

			editor.addCommand(KeyMod.CtrlCmd | KeyMod.Shift | KeyCode.Digit7, function () {
				// CMD + slash (toggle comment) on some EU keyboards
				editor?.trigger('keyboard', 'editor.action.commentLine', {})
			})
		})

		if (autoHeight) {
			const updateHeight = () => {
				const contentHeight = Math.min(1000, editor.getContentHeight())
				if (divEl) {
					divEl.style.height = `${contentHeight}px`
				}
				try {
					editor.layout({ width, height: contentHeight })
				} finally {
				}
			}
			editor.onDidContentSizeChange(updateHeight)
			updateHeight()
		}

		editor.onDidFocusEditorText(() => {
			editor.addCommand(KeyMod.CtrlCmd | KeyCode.KeyS, function () {
				code = getCode()
				shouldBindKey && format && format()
			})

			editor.addCommand(KeyMod.CtrlCmd | KeyCode.Enter, function () {
				code = getCode()
				shouldBindKey && cmdEnterAction && cmdEnterAction()
			})
			dispatch('focus')
		})

		editor.onDidBlurEditorText(() => {
			dispatch('blur')
			code = getCode()
		})

		if (lang === 'css' && !$cssClassesLoaded) {
			$cssClassesLoaded = true
			addCSSClassCompletions()
		}

		if (lang === 'tailwindcss' && !$tailwindClassesLoaded) {
			languages.register({ id: 'tailwindcss' })
			$tailwindClassesLoaded = true
			addTailwindClassCompletions()
		}

		if (placeholder) {
			editor.onDidChangeModelContent(() => {
				const value = editor.getValue()
				updatePlaceholderVisibility(value)
			})
		}
	}

	function addCSSClassCompletions() {
		languages.registerCompletionItemProvider('css', {
			provideCompletionItems: function (model, position, context, token) {
				const word = model.getWordUntilPosition(position)
				const range = {
					startLineNumber: position.lineNumber,
					startColumn: word.startColumn,
					endLineNumber: position.lineNumber,
					endColumn: word.endColumn
				}

				if (word && word.word) {
					const currentWord = word.word

					const suggestions = allClasses
						.filter((className) => className.includes(currentWord))
						.map((className) => ({
							label: className,
							kind: languages.CompletionItemKind.Class,
							insertText: className,
							documentation: 'Custom CSS class',
							range: range
						}))

					return { suggestions }
				}

				return { suggestions: [] }
			}
		})
	}

	function addTailwindClassCompletions() {
		languages.registerCompletionItemProvider('tailwindcss', {
			provideCompletionItems: function (model, position, context, token) {
				const word = model.getWordUntilPosition(position)
				const range = {
					startLineNumber: position.lineNumber,
					startColumn: word.startColumn,
					endLineNumber: position.lineNumber,
					endColumn: word.endColumn
				}

				if (word && word.word) {
					const currentWord = word.word

					const suggestions = tailwindClasses
						.filter((className) => className.includes(currentWord))
						.map((className) => ({
							label: className,
							kind: languages.CompletionItemKind.Class,
							insertText: className,
							documentation: 'Custom CSS class',
							range: range
						}))

					return { suggestions }
				}

				return { suggestions: [] }
			}
		})
	}

	function loadExtraLib() {
		if (lang == 'javascript') {
			const stdLib = { content: libStdContent, filePath: 'es6.d.ts' }
			const libs = [stdLib]
			if (domLib) {
				const domDTS = { content: domContent, filePath: 'dom.d.ts' }
				libs.push(domDTS)
			}
			if (extraLib != '') {
				libs.push({
					content: extraLib,
					filePath: 'windmill.d.ts'
				})
			}
			languages.typescript.javascriptDefaults.setExtraLibs(libs)
		}
	}

	let mounted = false
	onMount(async () => {
		if (BROWSER) {
			mounted = true
			await loadMonaco()
			if (autofocus) {
				setTimeout(() => {
					focus()
				}, 0)
			}
		}
	})

	$: mounted && extraLib && initialized && loadExtraLib()

	onDestroy(() => {
		try {
			vimDisposable?.dispose()
			model && model.dispose()
			editor && editor.dispose()
		} catch (err) {}
	})

	export function setCursorToEnd(): void {
		if (editor) {
			const lastLine = editor.getModel()?.getLineCount() ?? 1
			const lastColumn = editor.getModel()?.getLineMaxColumn(lastLine) ?? 1
			editor.setPosition({ lineNumber: lastLine, column: lastColumn })
			editor.focus()
		}
	}

	updatePlaceholderVisibility(code)
</script>

<EditorTheme />
{#if editor && suggestion && code.length === 0}
	<div
		class="absolute top-[0.05rem] left-[2.05rem] z-10 text-sm text-[#0007] italic font-mono dark:text-[#ffffff56] text-ellipsis overflow-hidden whitespace-nowrap"
		style={`max-width: calc(${width}px - 2.05rem)`}
	>
		{suggestion}
	</div>
{/if}
<div
	bind:this={divEl}
	class="relative {$$props.class ?? ''} editor simple-editor {!allowVim ? 'nonmain-editor' : ''}"
	bind:clientWidth={width}
>
	{#if placeholder}
		<div
			id="placeholder"
			class="absolute left-[24px] text-gray-500 text-sm pointer-events-none font-mono z-10 {placeholderVisible
				? ''
				: 'hidden'}"
		>
			{@html placeholder}
		</div>
	{/if}
</div>
{#if allowVim && $vimMode}
	<div class="fixed bottom-0 z-30" bind:this={statusDiv} />
{/if}

<style lang="postcss">
	.editor {
		@apply rounded-lg p-0;
	}

	.small-editor {
		/* stylelint-disable-next-line unit-allowed-list */
		height: 26vh;
	}

	.few-lines-editor {
		/* stylelint-disable-next-line unit-allowed-list */
		height: 100px;
	}
</style>
