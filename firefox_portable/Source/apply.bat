



REM Environment variables:
set TT_MOZ_SRC_DIR=%BUILDDIR%
set TT_PATCH_DIR=E:\Mozilla\tete009_patch\tete\Fx142.0




REM update compilation to use C++20 instead of C++17, and C23 instead of C17:
patch --binary -N %TT_MOZ_SRC_DIR%\build\moz.configure\toolchain.configure %TT_PATCH_DIR%\toolchain.configure.patch

REM rename variables named bool to avoid conflict with the bool keyword in C23:
patch --binary -N %TT_MOZ_SRC_DIR%\nsprpub\pr\src\io\prmapopt.c %TT_PATCH_DIR%\prmapopt.c.patch
patch --binary -N %TT_MOZ_SRC_DIR%\security\nss\lib\dev\ckhelper.c %TT_PATCH_DIR%\ckhelper.c.patch




REM filter out -std=, -std:, and /std: flags from MIDL preprocessor command:
patch --binary -N %TT_MOZ_SRC_DIR%\build\midl.py %TT_PATCH_DIR%\midl.py.patch




REM force link tmemutil.dll:
patch --binary -N %TT_MOZ_SRC_DIR%\toolkit\xre\nsWindowsWMain.cpp %TT_PATCH_DIR%\nsWindowsWMain.cpp.patch




REM enable passing flags to Cargo using CARGOFLAGS:
patch --binary -N %TT_MOZ_SRC_DIR%\build\moz.configure\rust.configure %TT_PATCH_DIR%\rust.configure.patch




REM add the PROFILE_GEN_SCRIPT environment variable to allow running the custom profile script for collecting profile data,
REM and add CSIR PGO support:
patch --binary -N %TT_MOZ_SRC_DIR%\moz.configure %TT_PATCH_DIR%\moz.configure.patch
patch --binary -N %TT_MOZ_SRC_DIR%\build\moz.configure\lto-pgo.configure %TT_PATCH_DIR%\lto-pgo.configure.patch
patch --binary -N %TT_MOZ_SRC_DIR%\python\mozbuild\mozbuild\build_commands.py %TT_PATCH_DIR%\build_commands.py.patch
patch --binary -N %TT_MOZ_SRC_DIR%\build\pgo\profileserver.py %TT_PATCH_DIR%\profileserver.py.patch
patch --binary -N %TT_MOZ_SRC_DIR%\testing\mozbase\mozhttpd\mozhttpd\mozhttpd.py %TT_PATCH_DIR%\mozhttpd.py.patch

patch --binary -N %TT_MOZ_SRC_DIR%\security\sandbox\common\SandboxSettings.h %TT_PATCH_DIR%\SandboxSettings.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\security\sandbox\common\SandboxSettings.cpp %TT_PATCH_DIR%\SandboxSettings.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\security\sandbox\win\src\sandboxbroker\sandboxBroker.cpp %TT_PATCH_DIR%\sandboxBroker.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\python\mozbuild\mozbuild\mozconfig.py %TT_PATCH_DIR%\mozconfig.py.patch
patch --binary -N %TT_MOZ_SRC_DIR%\config\config.mk %TT_PATCH_DIR%\config.mk.patch
patch --binary -N %TT_MOZ_SRC_DIR%\xpcom\base\nscore.h %TT_PATCH_DIR%\nscore.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\modules\libpref\init\StaticPrefList.yaml %TT_PATCH_DIR%\StaticPrefList.yaml.patch
patch --binary -N %TT_MOZ_SRC_DIR%\build\pure_virtual\moz.build %TT_PATCH_DIR%\pure_virtual_moz.build.patch
patch --binary -N %TT_MOZ_SRC_DIR%\config\makefiles\rust.mk %TT_PATCH_DIR%\rust.mk.patch
patch --binary -N %TT_MOZ_SRC_DIR%\config\rules.mk %TT_PATCH_DIR%\rules.mk.patch

patch --binary -N %TT_MOZ_SRC_DIR%\third_party\rust\cc\src\flags.rs %TT_PATCH_DIR%\cc_flags.rs.patch
patch --binary -N %TT_MOZ_SRC_DIR%\third_party\rust\cc\.cargo-checksum.json %TT_PATCH_DIR%\cc_cargo-checksum.json.patch




REM add the TT_FORCE_DISABLE_E10S environment variable to tete009 build to allow the forced disabling of e10s for debugging purposes:
patch --binary -N %TT_MOZ_SRC_DIR%\toolkit\xre\nsAppRunner.cpp %TT_PATCH_DIR%\nsAppRunner.cpp.patch

REM add the TT_FAKE_WEBDRIVER environment variable to tete009 build to always spoof navigator.webdriver as false when set:
patch --binary -N %TT_MOZ_SRC_DIR%\dom\base\Navigator.cpp %TT_PATCH_DIR%\Navigator.cpp.patch




REM generate the Visual Studio project files based on target CPU:
patch --binary -N %TT_MOZ_SRC_DIR%\python\mozbuild\mozbuild\backend\visualstudio.py %TT_PATCH_DIR%\visualstudio.py.patch

REM mach lint: fix failure on missing .hgignore in Jujutsu repositories:
patch --binary -N %TT_MOZ_SRC_DIR%\python\mozlint\mozlint\parser.py %TT_PATCH_DIR%\mozlint_parser.py.patch




REM memory allocator that retains allocations for the lifetime of the process:
patch --binary -N %TT_MOZ_SRC_DIR%\mozglue\misc\moz.build %TT_PATCH_DIR%\mozglue_misc_moz.build.patch
patch --binary -N %TT_MOZ_SRC_DIR%\mozglue\misc\AutoMemory.h %TT_PATCH_DIR%\AutoMemory.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\mozglue\misc\AutoMemory.cpp %TT_PATCH_DIR%\AutoMemory.cpp.patch




REM various size optimizations:
patch --binary -N %TT_MOZ_SRC_DIR%\third_party\aom\aom_dsp\odintrin.h %TT_PATCH_DIR%\odintrin.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\third_party\aom\aom_dsp\odintrin.c %TT_PATCH_DIR%\odintrin.c.patch

patch --binary -N %TT_MOZ_SRC_DIR%\js\src\vm\WellKnownAtom.h %TT_PATCH_DIR%\WellKnownAtom.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\js\src\vm\WellKnownAtom.cpp %TT_PATCH_DIR%\WellKnownAtom.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\intl\components\src\LocaleGenerated.cpp %TT_PATCH_DIR%\LocaleGenerated.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\media\libnestegg\src\nestegg.c %TT_PATCH_DIR%\nestegg.c.patch

patch --binary -N %TT_MOZ_SRC_DIR%\dom\svg\SVGFEBlendElement.h %TT_PATCH_DIR%\SVGFEBlendElement.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\dom\svg\SVGFEBlendElement.cpp %TT_PATCH_DIR%\SVGFEBlendElement.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\toolkit\components\aboutthirdparty\AboutThirdParty.cpp %TT_PATCH_DIR%\AboutThirdParty.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\image\SurfaceFilters.h %TT_PATCH_DIR%\SurfaceFilters.h.patch

patch --binary -N %TT_MOZ_SRC_DIR%\toolkit\components\places\nsNavHistory.cpp %TT_PATCH_DIR%\nsNavHistory.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\intl\locale\LocaleService.cpp %TT_PATCH_DIR%\LocaleService.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\caps\nsScriptSecurityManager.cpp %TT_PATCH_DIR%\nsScriptSecurityManager.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\dom\media\webrtc\transport\third_party\nICEr\src\stun\stun_codec.c %TT_PATCH_DIR%\stun_codec.c.patch

patch --binary -N %TT_MOZ_SRC_DIR%\gfx\skia\skia\src\core\SkOpts.h %TT_PATCH_DIR%\SkOpts.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\skia\skia\src\core\SkOpts.cpp %TT_PATCH_DIR%\SkOpts.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\skia\skia\src\opts\SkOpts_hsw.cpp %TT_PATCH_DIR%\SkOpts_hsw.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\gfx\skia\skia\src\base\SkArenaAlloc.h %TT_PATCH_DIR%\SkArenaAlloc.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\skia\skia\src\base\SkArenaAlloc.cpp %TT_PATCH_DIR%\SkArenaAlloc.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\gfx\thebes\StandardFonts-win10.inc %TT_PATCH_DIR%\StandardFonts-win10.inc.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\thebes\gfxDWriteFontList.h %TT_PATCH_DIR%\gfxDWriteFontList.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\thebes\gfxDWriteFontList.cpp %TT_PATCH_DIR%\gfxDWriteFontList.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\thebes\gfxPlatformFontList.h %TT_PATCH_DIR%\gfxPlatformFontList.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\thebes\gfxPlatformFontList.cpp %TT_PATCH_DIR%\gfxPlatformFontList.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\media\gmp-clearkey\0.1\gmp-clearkey.cpp %TT_PATCH_DIR%\gmp-clearkey.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\widget\windows\WinIMEHandler.h %TT_PATCH_DIR%\WinIMEHandler.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\widget\windows\WinIMEHandler.cpp %TT_PATCH_DIR%\WinIMEHandler.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\dom\canvas\SanitizeRenderer.cpp %TT_PATCH_DIR%\SanitizeRenderer.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\xpcom\base\ErrorList.py %TT_PATCH_DIR%\ErrorList.py.patch
patch --binary -N %TT_MOZ_SRC_DIR%\mozglue\baseprofiler\public\BaseProfilerMarkersPrerequisites.h %TT_PATCH_DIR%\BaseProfilerMarkersPrerequisites.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\dom\security\trusted-types\TrustedTypesConstants.h %TT_PATCH_DIR%\TrustedTypesConstants.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\angle\checkout\src\compiler\translator\ImmutableString.h %TT_PATCH_DIR%\ImmutableString.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\angle\checkout\src\compiler\translator\StaticType.h %TT_PATCH_DIR%\StaticType.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\dom\media\platforms\PlatformDecoderModule.h %TT_PATCH_DIR%\PlatformDecoderModule.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\toolkit\xre\GeckoArgs.h %TT_PATCH_DIR%\GeckoArgs.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\modules\libpref\Preferences.h %TT_PATCH_DIR%\Preferences.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\accessible\base\CacheConstants.h %TT_PATCH_DIR%\CacheConstants.h.patch




REM field reordering to reduce padding:
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\angle\checkout\src\compiler\translator\Types.h %TT_PATCH_DIR%\angle_translator_Types.h.patch




REM reducing code duplication across template instances:

REM ToString (-19KB):
patch --binary -N %TT_MOZ_SRC_DIR%\mfbt\moz.build %TT_PATCH_DIR%\mfbt_moz.build.patch
patch --binary -N %TT_MOZ_SRC_DIR%\mfbt\ToString.h %TT_PATCH_DIR%\ToString.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\mfbt\ToString.cpp %TT_PATCH_DIR%\ToString.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\dom\media\webrtc\sdp\ParsingResultComparer.cpp %TT_PATCH_DIR%\ParsingResultComparer.cpp.patch

REM WebGLTexelConversions (-1.3MB):
patch --binary -N %TT_MOZ_SRC_DIR%\dom\canvas\WebGLTexelConversions.cpp %TT_PATCH_DIR%\WebGLTexelConversions.cpp.patch

REM rlbox_wasm2c_sandbox::callback_interceptor (-28KB):
patch --binary -N %TT_MOZ_SRC_DIR%\third_party\rlbox_wasm2c_sandbox\include\rlbox_wasm2c_sandbox.hpp %TT_PATCH_DIR%\rlbox_wasm2c_sandbox.hpp.patch

REM dom::Promise (-20KB):
patch --binary -N %TT_MOZ_SRC_DIR%\dom\promise\Promise.h %TT_PATCH_DIR%\Promise.h.patch

REM EventMetric<K>::record_with_time (-700KB):
patch --binary -N %TT_MOZ_SRC_DIR%\toolkit\components\glean\api\src\private\event.rs %TT_PATCH_DIR%\event.rs.patch

REM OpenGL generator (-100KB?):
patch --binary -N %TT_MOZ_SRC_DIR%\third_party\rust\gl_generator\.cargo-checksum.json %TT_PATCH_DIR%\gl_generator_.cargo-checksum.json.patch
patch --binary -N %TT_MOZ_SRC_DIR%\third_party\rust\gl_generator\generators\struct_gen.rs %TT_PATCH_DIR%\gl_generator_struct_gen.rs.patch




REM define restricted pointer attribute:
patch --binary -N %TT_MOZ_SRC_DIR%\mfbt\Attributes.h %TT_PATCH_DIR%\Attributes.h.patch




REM js/src/gc/Marking.cpp:
patch --binary -N %TT_MOZ_SRC_DIR%\js\src\gc\Marking.cpp %TT_PATCH_DIR%\Marking.cpp.patch




REM gklayout:
patch --binary -N %TT_MOZ_SRC_DIR%\layout\generic\ReflowInput.cpp %TT_PATCH_DIR%\ReflowInput.cpp.patch

REM avoid crash at the time of printing when applying PGO:
patch --binary -N %TT_MOZ_SRC_DIR%\layout\generic\nsContainerFrame.cpp %TT_PATCH_DIR%\nsContainerFrame.cpp.patch




REM NULL pointer check for entry->GetRequest():
patch --binary -N %TT_MOZ_SRC_DIR%\image\imgLoader.cpp %TT_PATCH_DIR%\imgLoader.cpp.patch




REM 2D:
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\2d\2D.h %TT_PATCH_DIR%\2D.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\2d\Factory.cpp %TT_PATCH_DIR%\Factory.cpp.patch

REM convolve horizontally using SSSE3:
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\2d\SkConvolver.cpp %TT_PATCH_DIR%\SkConvolver.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\2d\ConvolutionFilterSSE2.cpp %TT_PATCH_DIR%\ConvolutionFilterSSE2.cpp.patch




REM prefetch:
patch --binary -N %TT_MOZ_SRC_DIR%\dom\base\AttrArray.h %TT_PATCH_DIR%\AttrArray.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\dom\base\Element.h %TT_PATCH_DIR%\Element.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\generic\nsIFrame.cpp %TT_PATCH_DIR%\nsIFrame.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\generic\nsBlockFrame.cpp %TT_PATCH_DIR%\nsBlockFrame.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\generic\ViewportFrame.cpp  %TT_PATCH_DIR%\ViewportFrame.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\gfx\skia\skia\src\base\SkRectMemcpy.h %TT_PATCH_DIR%\SkRectMemcpy.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\gfx\wr\swgl\src\composite.h %TT_PATCH_DIR%\composite.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\js\src\frontend\BytecodeEmitter.cpp %TT_PATCH_DIR%\BytecodeEmitter.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\xpcom\base\nsCycleCollector.cpp %TT_PATCH_DIR%\nsCycleCollector.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\xpcom\base\CycleCollectedJSRuntime.cpp %TT_PATCH_DIR%\CycleCollectedJSRuntime.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\layout\painting\nsDisplayList.cpp %TT_PATCH_DIR%\nsDisplayList.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\painting\nsDisplayList.h %TT_PATCH_DIR%\nsDisplayList.h.patch

patch --binary -N %TT_MOZ_SRC_DIR%\dom\base\DOMIntersectionObserver.cpp %TT_PATCH_DIR%\DOMIntersectionObserver.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\painting\RetainedDisplayListBuilder.cpp %TT_PATCH_DIR%\RetainedDisplayListBuilder.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\generic\nsFlexContainerFrame.cpp %TT_PATCH_DIR%\nsFlexContainerFrame.cpp.patch

patch --binary -N %TT_MOZ_SRC_DIR%\layout\forms\nsTextControlFrame.cpp %TT_PATCH_DIR%\nsTextControlFrame.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\generic\nsCanvasFrame.cpp %TT_PATCH_DIR%\nsCanvasFrame.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\generic\nsColumnSetFrame.cpp %TT_PATCH_DIR%\nsColumnSetFrame.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\generic\nsGridContainerFrame.cpp %TT_PATCH_DIR%\nsGridContainerFrame.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\tables\nsTableFrame.cpp %TT_PATCH_DIR%\nsTableFrame.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\tables\nsTableRowFrame.cpp %TT_PATCH_DIR%\nsTableRowFrame.cpp.patch
patch --binary -N %TT_MOZ_SRC_DIR%\layout\base\RestyleManager.cpp %TT_PATCH_DIR%\RestyleManager.cpp.patch




REM jemalloc:
patch --binary -N %TT_MOZ_SRC_DIR%\memory\build\mozjemalloc.cpp %TT_PATCH_DIR%\mozjemalloc.cpp.patch




REM avoid compile error for mozilla48:
patch --binary -N %TT_MOZ_SRC_DIR%\dom\canvas\WebGLTypes.h %TT_PATCH_DIR%\WebGLTypes.h.patch




REM nsILocalFileWin:
patch --binary -N %TT_MOZ_SRC_DIR%\xpcom\io\nsILocalFileWin.idl %TT_PATCH_DIR%\nsILocalFileWin.idl.patch
patch --binary -N %TT_MOZ_SRC_DIR%\xpcom\io\nsLocalFileWin.h %TT_PATCH_DIR%\nsLocalFileWin.h.patch
patch --binary -N %TT_MOZ_SRC_DIR%\xpcom\io\nsLocalFileWin.cpp %TT_PATCH_DIR%\nsLocalFileWin.cpp.patch




REM avoid build failures in unified build environments post-patch for Bug 1830038:
patch --binary -N %TT_MOZ_SRC_DIR%\dom\media\webrtc\transport\third_party\nICEr\src\net\transport_addr.h %TT_PATCH_DIR%\transport_addr.h.patch




REM Maybe a bug. A wait handle cannot be used in CloseHandle:
patch --binary -N %TT_MOZ_SRC_DIR%\widget\windows\WinRegistry.cpp %TT_PATCH_DIR%\WinRegistry.cpp.patch




