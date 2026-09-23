# Terminal coverage sweep — omega @906f03f41b

Method: every `machine` declared in each squalr package (regex over `module`+`machine` decls) probed with
`omega inspect-terminal --machine <fq> <pkg>/build.omg` under the fresh swarm-binaries binary.
VERIFIES = terminal machine lowers + verifies. DECLINE = `cannot lower` diagnostic (InvalidUnitMachinePlan / Unsupported).
DEPCHECK/LOCK = package check-level gate reached before machine verdict (not a Terminal verdict).

Working-tree measurement accommodations (NOT committed): git `revision:` for `omega-language-std` bumped
104950e8 -> 906f03f41b in squalr-engine-session/-targets/-targets-native/squalr-cli/squalr-tests (old rev
does not compile under the new toolchain); stale omega.lock removed for squalr-cli/-tests (update cannot
refresh through the targets-native dep failure). At the pinned rev those packages report std-check failures

Check-level blockers: squalr-engine-targets-native fails checked compilation itself (56 diagnostics:
`host.*` value calls unresolved + `Service` generic unknown — z4 in-flight fix). Everything depending on
it (session, engine, cli, tests, plugin-memory-view-dolphin) is gated there, not at Terminal.

plugins/* and root build.omg contain only package-boundary `build` machines — no terminal machines to sweep.

| package | machine | verdict | diagnostic class |
|---|---|---|---|
| squalr-cli | `src::cli::Cli::dec_places` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-cli | `src::cli::Cli::init` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-cli | `src::cli::Cli::is_exit_line` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-cli | `src::cli::Cli::run` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-cli | `src::cli::Cli::to_upper` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-cli | `src::cli::Cli::token_is_ci` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::collect_values_request_executor::CollectValuesRequestExecutor::execute` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::constraint_deanonymizer::ConstraintDeanonymizer::build_type_plan_list` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::element_scan_dispatcher::ElementScanChainDispatcher::append_filters` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::element_scan_dispatcher::ElementScanChainDispatcher::apply_plan` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::element_scan_dispatcher::ElementScanChainDispatcher::dispatch_collection` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::element_scan_dispatcher::ElementScanChainDispatcher::run_chain` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::element_scan_request_executor::ElementScanRequestExecutor::execute` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::element_scanner::ElementScannerDriver::collect_metadata` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::element_scanner::ElementScannerDriver::dispatch_region` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::element_scanner::ElementScannerDriver::scan_regions` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::element_scanner::ElementScannerDriver::scan_snapshot` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::privileged_command_executor::PrivilegedCommandExecutor::execute` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::scan_command_executor::ScanCommandExecutor::execute` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::scan_new_request_executor::ScanNewRequestExecutor::execute` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::scan_reset_request_executor::ScanResetRequestExecutor::execute` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::scan_results_command_executor::ScanResultsCommandExecutor::execute` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::scan_results_list_request_executor::ScanResultsListRequestExecutor::count_by_type` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::scan_results_list_request_executor::ScanResultsListRequestExecutor::count_results` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::scan_results_list_request_executor::ScanResultsListRequestExecutor::enumerate_all` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::scan_results_list_request_executor::ScanResultsListRequestExecutor::execute` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::scan_results_list_request_executor::ScanResultsListRequestExecutor::merge_sorted` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::add_memory_region` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::fill_from_supplied_source` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::fill_snapshot` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::get_region` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::get_region_count` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::new` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::command_executors::snapshot_value_collector::SnapshotValueCollector::collect_all_regions` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::squalr_engine::SqualrEngine::dispatch_command` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::squalr_engine::SqualrEngine::get_mode` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::squalr_engine::SqualrEngine::init` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::squalr_engine::SqualrEngine::init_privileged_shell` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::squalr_engine::SqualrEngine::new` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::squalr_engine::SqualrEngine::open_process` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::squalr_engine::SqualrEngine::supply_fixture` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine | `src::squalr_engine::SqualrEngine::supply_memory` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-api | `src::commands::command_line::command_line_parser::CommandLineParser::parse` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::com |
| squalr-engine-api | `src::commands::command_line::command_line_parser::find_equals` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::commands::command_line::command_line_parser::flag_is` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::commands::command_line::command_line_parser::flag_value` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::commands::command_line::command_line_parser::is_space` | VERIFIES |  —  |
| squalr-engine-api | `src::commands::command_line::command_line_parser::next_token` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::commands::command_line::command_line_parser::parse_scan` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::commands::command_line::command_line_parser::parse_scan_results` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::commands::command_line::command_line_parser::parse_u64` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::commands::command_line::command_line_parser::skip_space` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::commands::command_line::command_line_parser::token_end` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::commands::command_line::command_line_parser::token_is` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::commands::privileged_command_response::PrivilegedCommandResponse::get_result_address` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::commands::privileged_command_response::PrivilegedCommandResponse::get_result_count` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::commands::privileged_command_response::PrivilegedCommandResponse::get_result_value` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::commands::privileged_command_response::PrivilegedCommandResponse::is_scan` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::commands::privileged_command_response::PrivilegedCommandResponse::is_scan_results` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::commands::scan::collect_values::collect_values_response::CollectValuesResponse::default` | VERIFIES |  —  |
| squalr-engine-api | `src::commands::scan::element_scan::element_scan_request::ScanConstraintSet::empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::commands::scan::element_scan::element_scan_request::ScanConstraintSet::get` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::com |
| squalr-engine-api | `src::commands::scan::element_scan::element_scan_request::ScanConstraintSet::get_count` | VERIFIES |  —  |
| squalr-engine-api | `src::commands::scan::element_scan::element_scan_request::ScanConstraintSet::push` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::com |
| squalr-engine-api | `src::commands::scan::element_scan::element_scan_response::ElementScanResponse::default` | VERIFIES |  —  |
| squalr-engine-api | `src::commands::scan::new::scan_new_response::ScanNewResponse::default` | VERIFIES |  —  |
| squalr-engine-api | `src::commands::scan::reset::scan_reset_response::ScanResetResponse::default` | VERIFIES |  —  |
| squalr-engine-api | `src::commands::scan::scan_response::ScanResponse::is_element_scan` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::commands::scan::scan_response::ScanResponse::is_new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::commands::scan_results::list::scan_results_list_response::ScanResultPage::empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::commands::scan_results::list::scan_results_list_response::ScanResultPage::get` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::com |
| squalr-engine-api | `src::commands::scan_results::list::scan_results_list_response::ScanResultPage::get_count` | VERIFIES |  —  |
| squalr-engine-api | `src::commands::scan_results::list::scan_results_list_response::ScanResultPage::push` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::com |
| squalr-engine-api | `src::commands::scan_results::list::scan_results_list_response::ScanResultsListResponse::default` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::commands::scan_results::list::scan_results_list_response::ScanResultsListResponse::get_result_address` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::com |
| squalr-engine-api | `src::commands::scan_results::list::scan_results_list_response::ScanResultsListResponse::get_result_count` | VERIFIES |  —  |
| squalr-engine-api | `src::commands::scan_results::list::scan_results_list_response::ScanResultsListResponse::get_result_value` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::com |
| squalr-engine-api | `src::commands::scan_results::scan_results_response::ScanResultsResponse::get_result_address` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::com |
| squalr-engine-api | `src::commands::scan_results::scan_results_response::ScanResultsResponse::get_result_count` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::com |
| squalr-engine-api | `src::commands::scan_results::scan_results_response::ScanResultsResponse::get_result_value` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::com |
| squalr-engine-api | `src::commands::scan_results::scan_results_response::ScanResultsResponse::is_list` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::has_wildcards` | DECLINE | Unsupported: scalar graph structural formals require whole parameter transfers — other / stage= / omission= |
| squalr-engine-api | `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::hex_value` | VERIFIES |  —  |
| squalr-engine-api | `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::is_ascii_hexdigit` | DECLINE | PANIC: boolean-short-circuit-lowering (checked-trees-to-lowered-psi boolean.rs:204 unreachable) — other / stage= / omission= |
| squalr-engine-api | `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::is_ascii_whitespace` | VERIFIES |  —  |
| squalr-engine-api | `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::is_separator` | VERIFIES |  —  |
| squalr-engine-api | `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::parse` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::con |
| squalr-engine-api | `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::parse_consistent` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::con |
| squalr-engine-api | `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::uppercase_ascii` | DECLINE | PANIC: boolean-short-circuit-lowering (checked-trees-to-lowered-psi boolean.rs:204 unreachable) — other / stage= / omission= |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::binary_place` | DECLINE | Unsupported: direct scalar call target has an unsupported terminal signature — other / stage= / omission= |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::binary_scale` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: local data: scalar local: pure initializer — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: local data: scalar local: pur |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::binary_suffix` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::conversions::storage_ |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::format_rounded` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::matches` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::con |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::metric_place` | DECLINE | Unsupported: direct scalar call target has an unsupported terminal signature — other / stage= / omission= |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::metric_scale` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: local data: scalar local: pure initializer — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: local data: scalar local: pur |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::metric_suffix` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::conversions::storage_ |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::rounded_tenths` | VERIFIES |  —  |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::value_to_binary_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::con |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::value_to_metric_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::con |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::value_to_text_consistent` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeConversions::zero_b` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeText::get_byte` | DECLINE | Unsupported: indexed reads require a whole byte-view parameter — other / stage= / omission= |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeText::get_len` | VERIFIES |  —  |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeText::put_byte` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeText::put_digits_reversed` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeText::put_suffix` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::conversions::storage_size_conversions::StorageSizeText::reverse` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::plugins::memory_view::page_retrieval_mode::PageRetrievalMode::default` | VERIFIES |  —  |
| squalr-engine-api | `src::registries::scan_rules::pointer_scan_rule_registry::PointerScanRuleRegistry::get_instance` | VERIFIES |  —  |
| squalr-engine-api | `src::registries::scan_rules::pointer_scan_rule_registry::PointerScanRuleRegistry::map_pointer_scan_execution_plan` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::registries::scan_rules::pointer_scan_rule_registry::PointerScanRuleRegistry::new` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::copy_id_window` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::default` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::equals` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::get_base_data_type_id_len` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::get_data_type_id_byte` | DECLINE | Unsupported: indexed reads require a whole byte-view parameter — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::get_data_type_id_len` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::get_unit_size_in_bytes` | DECLINE | Unsupported: scalar computation needs one checked expression and one source binding — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::id_is` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::new_from_window` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::parse` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_types::data_type_ref::DataTypeRef::set_data_type_id` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::data_types::generics::vector_generics::VectorGenerics::plan_vector_scan` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: local data: scalar local: pure initializer — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: local data: scalar local: pur |
| squalr-engine-api | `src::structures::data_types::generics::vectorization_plan::VectorizationPlan::clone` | DECLINE | Unsupported: Unit graph borrowed parameter is not a primitive or byte slice — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_types::generics::vectorization_plan::VectorizationPlan::clone_from` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_types::generics::vectorization_plan::VectorizationPlan::equals` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_types::generics::vectorization_plan::VectorizationPlan::get_remainder_bytes` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_types::generics::vectorization_plan::VectorizationPlan::get_remainder_elements` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_types::generics::vectorization_plan::VectorizationPlan::get_remainder_ptr_offset` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_types::generics::vectorization_plan::VectorizationPlan::get_vectorizable_element_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_types::generics::vectorization_plan::VectorizationPlan::get_vectorizable_iterations` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_types::generics::vectorization_plan::VectorizationPlan::is_valid` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a local initializer — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a local in |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::copy_anonymous_value_string` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::copy_bytes` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::fill_value` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::from_str` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::from_str_consistent` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::get_anonymous_value_string_byte` | DECLINE | Unsupported: indexed reads require a whole byte-view parameter — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::get_anonymous_value_string_format` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::get_anonymous_value_string_len` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::get_container_type` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::new_window` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::parse` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::parse_u64` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: target state — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::set_anonymous_value_string` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::set_anonymous_value_string_format` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::AnonymousValueString::set_container_type` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string::holds` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string_format::AnonymousValueStringFormat::default` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string_format::AnonymousValueStringFormat::from_str` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string_format::AnonymousValueStringFormat::from_str_consistent` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string_format::AnonymousValueStringFormat::from_str_window` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string_format::AnonymousValueStringFormat::spelling` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::data_valu |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string_format::matches` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string_format::refused` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::anonymous_value_string_format::spelled` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::container_type::ContainerType::default` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::container_type::ContainerType::from_pointer_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_values::container_type::ContainerType::from_str` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_values::container_type::ContainerType::from_str_consistent` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::data_values::container_type::ContainerType::from_str_window` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_values::container_type::ContainerType::get_pointer_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_values::container_type::ContainerType::get_total_size_in_bytes` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a transition — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a transiti |
| squalr-engine-api | `src::structures::data_values::container_type::ContainerType::with_fixed_element_count` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_values::container_type::byte_is_space` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::container_type::index_of` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::container_type::mul10_add` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::container_type::parse_u64_window` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::container_type::saturating_mul` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::container_type::total` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::container_type::trim_left` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::container_type::trim_right` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::all` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::default` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::from_process_bitness` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::from_str` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::from_str_consistent` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::from_str_window` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::get_size_in_bytes` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::spelling` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::data_valu |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::ascii_lower` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::byte_is_space` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::matches_lower` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::refused` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::size_of` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::trim_left` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::data_values::pointer_scan_pointer_size::trim_right` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::address_display::ascii_eq_fold` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::address_display::ascii_lower` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::address_display::format_absolute_address` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::address_display::format_module_address` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::address_display::hex_digit_char` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::address_display::internal_resolved` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::address_display::is_virtual_module_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::address_display::offset_width` | DECLINE | Unsupported: scalar graph control must be acyclic — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::address_display::parse_gba_slot` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::address_display::try_resolve_virtual_module_address` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::address_display::work_resolved` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::address_display::write_hex_upper` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::address_display::write_hex_upper_at` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::bitness::Bitness::get_pointer_width` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::endian::Endian::default` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::endian::Endian::equals` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::memory::endian::Endian::get_label` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::memory_alignment::AlignmentParseResult::parsed_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::memory::memory_alignment::AlignmentSpelling::of` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::memory_alignment::AlignmentSpelling::parse` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::memory_alignment::MemoryAlignment::default` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::memory_alignment::MemoryAlignment::from` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::memory_alignment::MemoryAlignment::from_str` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::memory::memory_alignment::MemoryAlignment::from_str_consistent` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::memory::memory_alignment::MemoryAlignment::get_size_in_bytes` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::memory_alignment::MemoryAlignmentParse::get_size` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::memory_alignment::MemoryAlignmentParse::is_ok` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::contains_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::get_base_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::get_base_region` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::get_module_address_display` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::get_module_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::n |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::get_region_size` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::into_base_region` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::new_from_normalized_region` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::new_from_normalized_region_with_display` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::new_with_display` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::set_base_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::set_module_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::memory::normalized_module::NormalizedModule::set_region_size` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::TotalOrder` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::base_address_order` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::clone` | DECLINE | Unsupported: Unit graph borrowed parameter is not a primitive or byte slice — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::clone_from` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::contains_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::equals` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::expand` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::get_base_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::get_end_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::get_region_size` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::new` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::set_alignment` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::set_base_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::set_base_address_retain_end_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::set_end_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::NormalizedRegion::set_region_size` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::normalized_region::equals` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::structures::memory::normalized_region::equals") |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::get_address` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::get_module_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::p |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::get_offset_count` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::get_offset_segments` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::p |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::get_offsets` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::get_pointer_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::get_root_display_text` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::has_symbolic_offsets` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::p |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::new_with_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::p |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::new_with_size_and_segments` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::p |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::set_address` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::set_module_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::memory::pointer::Pointer::set_pointer_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::memory::pointer::copy_text` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::pointer_chain_segment::offsets_to_pointer_chain_segments` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::ensure_minimum_links` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_link_count` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_links` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::s |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_module_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::s |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_numeric_root_offset` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_numeric_tail_offsets` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_pointer_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_tail_links` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::has_symbolic_links` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::is_empty` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::s |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::new_absolute` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::s |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::new_allow_empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::memory::s |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::set_module_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::set_pointer_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::as_offset` | DECLINE | Unsupported: composed Unit attachment is not a record — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::display_text` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::from_str` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::get_symbol_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::is_symbol` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::new_offset` | DECLINE | InvalidTerminalModule — InvalidTerminalModule / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::new_symbol` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::copy_symbol_text` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::hex_value` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::hex_width` | DECLINE | Unsupported: scalar graph control must be acyclic — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::symbolic_pointer_chain_apply_pointer_offset` | DECLINE | Unsupported: signed wrapping conversion requires runtime policy realization — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::symbolic_pointer_chain_format_offset` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::symbolic_pointer_chain_is_valid_symbol_name` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::symbolic_pointer_chain_parse_offset` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::memory::symbolic_pointer_chain::write_prefixed_hex` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_address_space::PointerScanAddressSpace::from_str` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_address_space::PointerScanAddressSpace::get_display_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::pointer_s |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_address_space::PointerScanAddressSpace::get_label` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::pointer_s |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_address_space::ascii_eq` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_address_space::lower_of` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_candidate::PointerScanCandidate::get_candidate_id` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_candidate::PointerScanCandidate::get_discovery_depth` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_candidate::PointerScanCandidate::get_module_index` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_candidate::PointerScanCandidate::get_module_offset` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_candidate::PointerScanCandidate::get_pointer_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_candidate::PointerScanCandidate::get_pointer_scan_node_type` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_candidate::PointerScanCandidate::get_pointer_value` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_candidate::PointerScanCandidate::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: structural result: returned value — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: structural result: returned v |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level::PointerScanLevel::get_depth` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level::PointerScanLevel::get_heap_node_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level::PointerScanLevel::get_node_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level::PointerScanLevel::get_static_node_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level::PointerScanLevel::new` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::contains_static_candidate` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::ensure_heap_candidates_sorted` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::find_heap_candidate_by_address` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: target state — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::find_heap_candidates_in_range` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_discovery_depth` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_heap_candidates` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::pointer_s |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_heap_node_count` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_node_count` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_static_candidates` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::pointer_s |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_static_node_count` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::new_presorted` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::pointer_s |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::shift_heap_insert` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_candidates::shift_static_insert` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_summary::PointerScanLevelSummary::get_depth` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_summary::PointerScanLevelSummary::get_heap_node_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_summary::PointerScanLevelSummary::get_node_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_summary::PointerScanLevelSummary::get_static_node_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_level_summary::PointerScanLevelSummary::new` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_branch_total_depth` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_child_node_ids` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::pointer_s |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_depth` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_discovery_depth` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_graph_node_id` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_module_display_text` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_module_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::pointer_s |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_module_offset` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_node_id` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_parent_node_id` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_pointer_address` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_pointer_offset` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_pointer_scan_node_type` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_pointer_value` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_resolved_target_address` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::has_children` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::has_parent_node_id` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::pointer_s |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::new_materialized` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::pointer_s |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::set_branch_total_depth` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::set_depth` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::set_discovery_depth` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-api | `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::set_module_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::processes::opened_process_info::OpenedProcessInfo::get_bitness` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::processes::opened_process_info::OpenedProcessInfo::get_handle` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::opened_process_info::OpenedProcessInfo::get_name_len` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::opened_process_info::OpenedProcessInfo::get_pointer_width` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::opened_process_info::OpenedProcessInfo::get_process_id` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::opened_process_info::OpenedProcessInfo::get_process_id_raw` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::opened_process_info::OpenedProcessInfo::get_target_architecture` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::processes::opened_process_info::OpenedProcessInfo::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::processes::opened_process_info::OpenedProcessInfo::set_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::processes::opened_process_info::OpenedProcessInfo::with_target_architecture` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::processes::process_info::ProcessInfo::get_is_windowed` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::process_info::ProcessInfo::get_name_len` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::process_info::ProcessInfo::get_process_id` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::process_info::ProcessInfo::get_process_id_raw` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::process_info::ProcessInfo::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::processes::process_info::ProcessInfo::new_named` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::processes::process_info::ProcessInfo::set_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::processes::target_architecture::TargetArchitecture::arm64` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::target_architecture::TargetArchitecture::default_for_bitness` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::target_architecture::TargetArchitecture::get_pointer_width` | DECLINE | Unsupported: composed Unit attachment is not a record — other / stage= / omission= |
| squalr-engine-api | `src::structures::processes::target_architecture::TargetArchitecture::x64` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::processes::target_architecture::TargetArchitecture::x86` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::CursorProbe::inactive` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::CursorProbe::smaller` | DECLINE | Unsupported: Unit graph borrowed parameter is not a primitive or byte slice — other / stage= / omission= |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::DataTypeResultCounts::empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::DataTypeResultCounts::fill` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::DataTypeResultCounts::get` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::DataTypeResultCounts::get_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::DataTypeResultCounts::merge_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: jump successor: parameter transfer — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: jump successor: paramete |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::MergeCursors::get_cursor` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::MergeCursors::set_cursor` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::MergeCursors::unfinished` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElement::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a local initializer — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a local in |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElement::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElement::of` | DECLINE | InvalidTerminalModule — InvalidTerminalModule / stage= / omission= |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElementList::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElementList::copy_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElementList::empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElementList::get_element_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElementList::get_page_element` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElementList::insert_sorted` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElementList::push` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::PageElementList::shift_down` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::ResultCursor::active` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::ResultCursor::clone` | DECLINE | Unsupported: Unit graph borrowed parameter is not a primitive or byte slice — other / stage= / omission= |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::ResultCursor::clone_from` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::ResultCursor::finished` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::advance_cursor` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::copy_collections` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::enumerate_page` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::get_collection_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::get_filter_collection` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: structural operands — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: structural operands / omission=src:: |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::get_number_of_results` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::get_number_of_results_for_data_types` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::get_result_counts_by_data_type` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::is_data_type_in_set` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::probe_cursor` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: target state — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::push_collection` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::set_filter_collection` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::results::snapshot_region_scan_results::is_data_type_selected` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::scan_results::scan_result::ScanResult::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scan_results::scan_result::ScanResult::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: assignment: call source result type — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: assignment: call source resul |
| squalr-engine-api | `src::structures::scan_results::scan_result::ScanResult::default` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::scan_results::scan_result::ScanResult::get_address` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scan_results::scan_result::ScanResult::get_current_value` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scan_results::scan_result::ScanResult::is_valued` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scan_results::scan_result_base::ScanResultBase::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a local initializer — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a local in |
| squalr-engine-api | `src::structures::scan_results::scan_result_base::ScanResultBase::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::scan_results::scan_result_base::ScanResultBase::copy_icon` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::scan_results::scan_result_base::ScanResultBase::default` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::scan_results::scan_result_base::ScanResultBase::get_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_base::ScanResultBase::get_data_type_ref` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scan_results::scan_result_base::ScanResultBase::get_handle` | DECLINE | Unsupported: Unit graph borrowed parameter is not a primitive or byte slice — other / stage= / omission= |
| squalr-engine-api | `src::structures::scan_results::scan_result_base::ScanResultBase::get_icon_id_len` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_base::ScanResultBase::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scan_results::scan_result_base::ScanResultBase::set_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_data_type_count::ScanResultDataTypeCount::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scan_results::scan_result_data_type_count::ScanResultDataTypeCount::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::scan_results::scan_result_data_type_count::ScanResultDataTypeCount::default` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scan_results::scan_result_data_type_count::ScanResultDataTypeCount::new` | DECLINE | InvalidTerminalModule — InvalidTerminalModule / stage= / omission= |
| squalr-engine-api | `src::structures::scan_results::scan_result_ref::ScanResultRef::clone` | DECLINE | Unsupported: Unit graph borrowed parameter is not a primitive or byte slice — other / stage= / omission= |
| squalr-engine-api | `src::structures::scan_results::scan_result_ref::ScanResultRef::clone_from` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_ref::ScanResultRef::default` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_ref::ScanResultRef::get_is_struct` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_ref::ScanResultRef::get_scan_result_index` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_ref::ScanResultRef::new` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_ref::ScanResultRef::set_is_struct` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_ref::ScanResultRef::set_scan_result_index` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_valued::ScanResultValued::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a local initializer — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a local in |
| squalr-engine-api | `src::structures::scan_results::scan_result_valued::ScanResultValued::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::scan_results::scan_result_valued::ScanResultValued::default` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::scan_results::scan_result_valued::ScanResultValued::get_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_valued::ScanResultValued::get_base_result` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a local initializer — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a local in |
| squalr-engine-api | `src::structures::scan_results::scan_result_valued::ScanResultValued::get_current_value` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_valued::ScanResultValued::get_previous_value` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_valued::ScanResultValued::has_current_value` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_valued::ScanResultValued::has_previous_value` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_result_valued::ScanResultValued::new` | DECLINE | InvalidTerminalModule — InvalidTerminalModule / stage= / omission= |
| squalr-engine-api | `src::structures::scan_results::scan_results_metadata::ScanResultsMetadata::clone` | DECLINE | Unsupported: Unit graph borrowed parameter is not a primitive or byte slice — other / stage= / omission= |
| squalr-engine-api | `src::structures::scan_results::scan_results_metadata::ScanResultsMetadata::clone_from` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_results_metadata::ScanResultsMetadata::default` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_results_metadata::ScanResultsMetadata::get_result_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_results_metadata::ScanResultsMetadata::get_total_size_in_bytes` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_results_metadata::ScanResultsMetadata::set_result_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scan_results::scan_results_metadata::ScanResultsMetadata::set_total_size_in_bytes` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::comparisons::scan_compare_type::ScanCompareType::compare` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::comparisons::scan_compare_type::ScanCompareType::from_str` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::comparisons::scan_compare_type::ScanCompareType::from_str_consistent` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::scanning::comparisons::scan_compare_type::ScanCompareTypeParseResult::variant_probe` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::comparisons::scan_compare_type_delta::ScanCompareTypeDelta::compare` | DECLINE | OperationProofUnavailable — other / stage= / omission= |
| squalr-engine-api | `src::structures::scanning::comparisons::scan_compare_type_immediate::ScanCompareTypeImmediate::compare` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::comparisons::scan_compare_type_relative::ScanCompareTypeRelative::compare` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::get_anonymous_value_string` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a local initializer — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a local in |
| squalr-engine-api | `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::get_scan_compare_type` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::has_value` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::new_no_value` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::parse` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::clone` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::clone_consistent` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::clone_from` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::equals` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::get_base_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::get_element_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::get_end_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::get_misaligned_starting_byte_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::get_region_size` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::new` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::set_base_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::set_end_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::debug_assertion_parity_smoke` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter::equals` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::structures::scanning::filters::snapshot_region_filter::equals") |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::clamp_hi` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::clamp_lo` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a local initializer — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a local in |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::copy_filters` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::covered_in_range` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::from_single_filter` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a local initializer — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a local in |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_data_type_ref` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_filter` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_filter_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_filter_maximum_address` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_filter_minimum_address` | DECLINE | Unsupported: record operand has no named or projected source — other / stage= / omission= |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_memory_alignment` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_number_of_results` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_result_value_size_in_bytes` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::locate_result` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: target state — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::new_with_result_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::overlap` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::push_filter` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::retain_result_sized_filters` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter custody shape: owned non-linear unnamed type — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: parameter custody s |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::set_filter` | DECLINE | InvalidUnitMachinePlan @  — InvalidUnitMachinePlan / stage= / omission=src::structures::scanning::filters::snapshot_region_filter_collecti |
| squalr-engine-api | `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::sort_filters` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: guarded jump successors: roster — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: guarded jump successors: |
| squalr-engine-api | `src::structures::scanning::memory_read_mode::MemoryReadMode::default` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::memory_read_mode::MemoryReadMode::from_str` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::clone_data_type_refs` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_data_type_ref` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_data_type_ref_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_is_single_threaded_scan` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_memory_alignment` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_memory_read_mode` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_plan_list` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_plan_list_for` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::push_type_plans` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::get_plan` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::get_plan_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::push` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::default` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::get_memory_alignment` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::get_operand_value` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::get_planned_scan_type` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::get_scan_compare_type` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::get_scan_function_scalar` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::get_unit_size_in_bytes` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::has_scan_function_scalar` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::set_planned_scan_type` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::planned_pointer_scan_kernel_kind::PlannedPointerScanKernelKind::get_display_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::scanning: |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_execution_plan::PointerScanExecutionPlan::get_frontier_target_range_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_execution_plan::PointerScanExecutionPlan::get_planned_kernel_kind` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_execution_plan::PointerScanExecutionPlan::get_pointer_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_execution_plan::PointerScanExecutionPlan::get_scan_region_byte_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_execution_plan::PointerScanExecutionPlan::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: structural result: returned value — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: structural result: returned v |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_execution_plan::PointerScanExecutionPlan::set_planned_kernel_kind` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_parameters::PointerScanParameters::get_debug_perform_validation_scan` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_parameters::PointerScanParameters::get_is_single_thread_scan` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_parameters::PointerScanParameters::get_max_depth` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_parameters::PointerScanParameters::get_offset_radius` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_parameters::PointerScanParameters::get_pointer_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::scanning::plans::pointer_scan::pointer_scan_parameters::PointerScanParameters::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: structural result: returned value — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: structural result: returned v |
| squalr-engine-api | `src::structures::scanning::rules::pointer_scan::built_in_planning_rules::rule_map_search_kernel::RuleMapSearchKernel::get_id` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::scanning: |
| squalr-engine-api | `src::structures::scanning::rules::pointer_scan::built_in_planning_rules::rule_map_search_kernel::RuleMapSearchKernel::map_plan` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: target state — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::scanning::rules::pointer_scan::built_in_planning_rules::rule_map_search_kernel::RuleMapSearchKernel::rule_id` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::scanning: |
| squalr-engine-api | `src::structures::scanning::rules::pointer_scan::built_in_planning_rules::rule_map_search_kernel::RuleMapSearchKernel::select_kernel_kind` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: target state — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::scanning::rules::pointer_scan_planning_rule::get_id` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::structures::scanning::rules::pointer_scan_planning_rule::get_id") |
| squalr-engine-api | `src::structures::scanning::rules::pointer_scan_planning_rule::map_plan` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::structures::scanning::rules::pointer_scan_planning_rule::map_plan") |
| squalr-engine-api | `src::structures::settings::scan_settings::ScanSettings::default` | DECLINE | InvalidTerminalModule — InvalidTerminalModule / stage= / omission= |
| squalr-engine-api | `src::structures::settings::scan_settings::ScanSettings::get_is_single_threaded_scan` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::settings::scan_settings::ScanSettings::get_memory_alignment` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::settings::scan_settings::ScanSettings::get_memory_read_mode` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::settings::scan_settings::ScanSettings::get_results_page_size` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::clear` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::copy_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::get_covered_byte_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::get_element` | DECLINE | Unsupported: scalar computation needs one checked expression and one source binding — other / stage= / omission= |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::get_element_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::is_empty` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::of_length` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::push_element` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::set_element` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::slice` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::truncate_back` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::element_window::ElementWindow::truncate_front` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::apply_region_scan_results` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: edge cleanup — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::clear` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::collect_region_values` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: edge cleanup — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::discard_empty_regions` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: prefix initializers: bound expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: prefix initializers: bound expressio |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::get_collected_byte_count` | DECLINE | Unsupported: scalar computation needs one checked expression and one source binding — other / stage= / omission= |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::get_region` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::get_region_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::initialize_all_scan_results` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: edge cleanup — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::push_region` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::set_region` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: edge cleanup — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::set_snapshot_regions` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter custody shape: borrowed non-view carrier — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: parameter custody s |
| squalr-engine-api | `src::structures::snapshots::snapshot::Snapshot::store_regions` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter custody shape: borrowed non-view carrier — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: parameter custody s |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::DataTypeRefSet::empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::DataTypeRefSet::get` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::DataTypeRefSet::get_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::DataTypeRefSet::push` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::clone_from` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::compute_filter_bounds` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::copy_boundaries` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::covered_by_filters` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::from_elements` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a call statement — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a call sta |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_base_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_collected_byte_count` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a local initializer — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a local in |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_current_element` | DECLINE | Unsupported: scalar computation needs one checked expression and one source binding — other / stage= / omission= |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_current_element_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_current_values_slice` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::snapshots |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_end_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_normalized_region` | DECLINE | Unsupported: Unit graph borrowed parameter is not a primitive or byte slice — other / stage= / omission= |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_page_boundary` | DECLINE | Unsupported: scalar computation needs one checked expression and one source binding — other / stage= / omission= |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_page_boundary_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_previous_element` | DECLINE | Unsupported: scalar computation needs one checked expression and one source binding — other / stage= / omission= |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_previous_element_count` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_previous_values_slice` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::snapshots |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_region_size` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::get_scan_results` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::has_current_values` | DECLINE | Unsupported: scalar computation needs one checked expression and one source binding — other / stage= / omission= |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::initialize_scan_results` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::pick_max` | DECLINE | PANIC: boolean-short-circuit-lowering (checked-trees-to-lowered-psi boolean.rs:204 unreachable) — other / stage= / omission= |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::pick_min` | DECLINE | PANIC: boolean-short-circuit-lowering (checked-trees-to-lowered-psi boolean.rs:204 unreachable) — other / stage= / omission= |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::push_page_boundary` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::str |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::resize_to_filters` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::rotate_values_for_collection` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::set_base_address` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::set_current_values` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type — InvalidUnitMachinePlan / stage=local construction stopped at structural field store: scalar field type / omiss |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::set_region_size` | VERIFIES |  —  |
| squalr-engine-api | `src::structures::snapshots::snapshot_region::SnapshotRegion::set_scan_results` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: call: call operation / omissi |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::cancel` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at signature — InvalidUnitMachinePlan / stage=local construction stopped at signature / omission=src::structures::tasks::trac |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::complete` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at signature — InvalidUnitMachinePlan / stage=local construction stopped at signature / omission=src::structures::tasks::trac |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::create` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::tasks::tr |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::get_cancellation_token` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at signature — InvalidUnitMachinePlan / stage=local construction stopped at signature / omission=src::structures::tasks::trac |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::get_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::tasks::tr |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::get_progress` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at signature — InvalidUnitMachinePlan / stage=local construction stopped at signature / omission=src::structures::tasks::trac |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::get_task_handle` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::tasks::tr |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::get_task_identifier` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::tasks::tr |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::is_completed` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at signature — InvalidUnitMachinePlan / stage=local construction stopped at signature / omission=src::structures::tasks::trac |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::next_progress_update` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter signature: attached data shape — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: parameter signature |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::set_name` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at signature — InvalidUnitMachinePlan / stage=local construction stopped at signature / omission=src::structures::tasks::trac |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::set_progress` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter signature: attached data shape — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: parameter signature |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::set_task_identifier` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at signature — InvalidUnitMachinePlan / stage=local construction stopped at signature / omission=src::structures::tasks::trac |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::subscribe_to_progress_updates` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at signature — InvalidUnitMachinePlan / stage=local construction stopped at signature / omission=src::structures::tasks::trac |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::wait_for_completion` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter signature: attached data shape — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: parameter signature |
| squalr-engine-api | `src::structures::tasks::trackable_task::TrackableTask::wait_for_progress_update` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter signature: attached data shape — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: parameter signature |
| squalr-engine-api | `src::structures::tasks::trackable_task::copy_task_text` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-api | `src::structures::tasks::trackable_task_handle::TrackableTaskHandle::clone` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::structures::tasks::tr |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_byte_at` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_pointer_lane_values_u32` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_pointer_lane_values_u64` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_pointer_value_unchecked` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_24_be` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::poi |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_24_le` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::poi |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_32_be` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::poi |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_32_le` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::poi |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_64_be` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::poi |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_64_le` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::poi |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_scalar_binary_search_kernel::ScalarBinaryPointerScanKernel::is_empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: local data: structural result shape — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: local data: structural result |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_scalar_binary_search_kernel::ScalarBinaryPointerScanKernel::scan_region_with_visitor` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter signature: structural parameter type — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: parameter signature |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_scalar_linear_search_kernel::ScalarLinearPointerScanKernel::is_empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: local data: structural result shape — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: local data: structural result |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_scalar_linear_search_kernel::ScalarLinearPointerScanKernel::scan_region_with_visitor` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter signature: structural parameter type — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: parameter signature |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_scalar_region_scanner::scan_region_scalar_with_predicate` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_search_kernel_context::PointerScanSearchKernelContext::get_pointer_size` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_search_kernel_context::PointerScanSearchKernelContext::get_target_range_set` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::pointer_scans::search |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_search_kernel_context::PointerScanSearchKernelContext::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::pointer_scans::search |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_search_kernel_utils::find_scan_start_offset` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_simd_linear_search_kernel::SimdLinearPointerScanKernel::is_empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: local data: structural result shape — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: local data: structural result |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_simd_linear_search_kernel::SimdLinearPointerScanKernel::scan_region_with_visitor` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter signature: structural parameter type — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: parameter signature |
| squalr-engine-scanning | `src::pointer_scans::search_kernels::pointer_scan_simd_linear_search_kernel::visit` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::pointer_scans::search_kernels::pointer_scan_simd_linear_search_kernel::visit") |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_collected_level::PointerScanCollectedLevel::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::pointer_scans::struct |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_collected_level::PointerScanCollectedLevel::push_heap` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_collected_level::PointerScanCollectedLevel::push_static` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: conditional successors:  |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_region_match::PointerScanRegionMatch::get_pointer_address` | VERIFIES |  —  |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_region_match::PointerScanRegionMatch::get_pointer_value` | VERIFIES |  —  |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_region_match::PointerScanRegionMatch::new` | VERIFIES |  —  |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeBucket::get_bucket_key` | VERIFIES |  —  |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeBucket::get_end_range_index_exclusive` | VERIFIES |  —  |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeBucket::get_start_range_index` | VERIFIES |  —  |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeBucket::new` | VERIFIES |  —  |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeBucket::set_end_range_index_exclusive` | VERIFIES |  —  |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeSet::empty` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::pointer_scans::struct |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeSet::from_sorted_target_addresses` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::poi |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeSet::from_target_addresses` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::poi |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeSet::get_source_target_count` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::pointer_scan_target_range_set_contains_value_binary` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::pointer_scan_target_range_set_contains_value_linear` | DECLINE | Unsupported: machine has no source-independent checked scalar control plan — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::pointer_scan_target_range_set_get_range_count` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::pointer_scan_target_range_set_is_empty` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-scanning | `src::pointer_scans::structures::pointer_scan_target_ranges::target_range_upper_max` | VERIFIES |  —  |
| squalr-engine-scanning | `src::pointer_scans::structures::snapshot_region_scan_task::SnapshotRegionScanTasks::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::pointer_scans::struct |
| squalr-engine-scanning | `src::scanners::element_scan_dispatcher::ElementScanDispatcher::dispatch_scalar_region` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::sca |
| squalr-engine-scanning | `src::scanners::element_scan_dispatcher::ScalarRegionScan::next` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::sca |
| squalr-engine-scanning | `src::scanners::element_scan_runner::ElementScanRunner::drain_iterative` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: guarded jump successors: roster — InvalidUnitMachinePlan / stage=local construction stopped at state graph: terminator: guarded jump successors: |
| squalr-engine-scanning | `src::scanners::element_scan_runner::ElementScanRunner::run_region` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::sca |
| squalr-engine-scanning | `src::scanners::scalar::scanner_scalar_iterative::ScalarIterativeScan::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: ordered statement call / omission=sr |
| squalr-engine-scanning | `src::scanners::scalar::scanner_scalar_iterative::ScalarIterativeScan::next` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::sca |
| squalr-engine-scanning | `src::scanners::scalar::scanner_scalar_single_element::ScannerScalarSingleElement::scan_region` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::sca |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::build_table` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: contract shape unadmitted — InvalidUnitMachinePlan / stage=local construction stopped at state graph: state signature: contract shape unad |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::get_aligned_pattern_length` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::get_good_suffix_shift` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::get_mismatch_shift` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::get_safe_mismatch_shift` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a transition — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a transiti |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::is_prefix` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::sca |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::mismatch_absent` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::mismatch_case` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind — InvalidUnitMachinePlan / stage=local construction stopped at statement sequence: unsupported statement kind /  |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::mismatch_present` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a transition — InvalidUnitMachinePlan / stage=local construction stopped at outer calls: unconsumed nested call in a transiti |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::new` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at result type — InvalidUnitMachinePlan / stage=local construction stopped at result type / omission=src::scanners::structures: |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::round_up_to_alignment` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::suffix_length` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::sca |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::u64_max` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-scanning | `src::scanners::structures::boyer_moore_table::BoyerMooreTable::u64_min` | DECLINE | Unsupported: borrowed slice view has no Terminal descriptor — other / stage= / omission= |
| squalr-engine-scanning | `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::encode_range` | VERIFIES |  —  |
| squalr-engine-scanning | `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::finalize_current_encode` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::sca |
| squalr-engine-scanning | `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::finalize_current_encode_with_minimum_size_filtering` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::sca |
| squalr-engine-scanning | `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::finalize_current_encode_with_padding` | DECLINE | InvalidUnitMachinePlan @ local construction stopped at state graph: result signature — InvalidUnitMachinePlan / stage=local construction stopped at state graph: result signature / omission=src::sca |
| squalr-engine-scanning | `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::get_current_address` | VERIFIES |  —  |
| squalr-engine-scanning | `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::get_current_run_length` | VERIFIES |  —  |
| squalr-engine-scanning | `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::is_encoding` | VERIFIES |  —  |
| squalr-engine-scanning | `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::new` | VERIFIES |  —  |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::borrow_snapshot` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::borrow_snapshot_mut` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::borrow_supplied_memory_source_mut` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::clear_freeze_list` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::clear_opened_process` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::get_freeze_list_count` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::get_opened_process` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::get_scan_settings` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::get_scan_settings_ref` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::get_snapshot` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::get_supplied_memory_source` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::has_opened_process` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::init` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::make_fixture_source` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::new` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::set_opened_process` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::set_scan_settings` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::set_snapshot` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::engine_privileged_state::EnginePrivilegedState::set_supplied_memory_source` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedMemorySource::clone_from` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedMemorySource::empty` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedMemorySource::get_page_bounds` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedMemorySource::get_region_count` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedMemorySource::of_region` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedMemorySource::push_region` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedMemorySource::read_u64` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedMemorySource::read_window` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedRegion::clone` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedRegion::clone_from` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedRegion::get_base_address` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedRegion::get_elements` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedRegion::get_region_size` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedRegion::new` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-session | `src::os::supplied_memory_source::SuppliedRegion::of_window` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets | `src::process_query::process_query_error::ProcessQueryError::close_process_failed` | VERIFIES |  —  |
| squalr-engine-targets | `src::process_query::process_query_error::ProcessQueryError::internal` | VERIFIES |  —  |
| squalr-engine-targets | `src::process_query::process_query_error::ProcessQueryError::not_implemented` | VERIFIES |  —  |
| squalr-engine-targets | `src::process_query::process_query_error::ProcessQueryError::open_process_failed` | VERIFIES |  —  |
| squalr-engine-targets | `src::process_query::process_query_error::ProcessQueryError::process_monitor_lock_poisoned` | VERIFIES |  —  |
| squalr-engine-targets | `src::process_query::process_query_options::ProcessQueryOptions::default` | DECLINE | InvalidTerminalModule — InvalidTerminalModule / stage= / omission= |
| squalr-engine-targets | `src::target_providers::close_page_bounds` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::close_page_bounds") |
| squalr-engine-targets | `src::target_providers::close_process` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::close_process") |
| squalr-engine-targets | `src::target_providers::get_processes` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::get_processes") |
| squalr-engine-targets | `src::target_providers::is_address_writable` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::is_address_writable") |
| squalr-engine-targets | `src::target_providers::is_process_alive` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::is_process_alive") |
| squalr-engine-targets | `src::target_providers::next_page_bounds_region` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::next_page_bounds_region") |
| squalr-engine-targets | `src::target_providers::open_page_bounds` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::open_page_bounds") |
| squalr-engine-targets | `src::target_providers::open_process` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::open_process") |
| squalr-engine-targets | `src::target_providers::read_bytes` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::read_bytes") |
| squalr-engine-targets | `src::target_providers::start_monitoring` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::start_monitoring") |
| squalr-engine-targets | `src::target_providers::stop_monitoring` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::stop_monitoring") |
| squalr-engine-targets | `src::target_providers::write_bytes` | NOT_FOUND | NOT_FOUND: trait-signature decls (no concrete machine name) — MachineNotFound("src::target_providers::write_bytes") |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::acquire_maps` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::base_in_modules` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::buf_byte_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::buf_put` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::byte_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::canon_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::canon_path` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::canon_set` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::consume_line_position` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::emit_min` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::fill_module` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::hash_path` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::hex_digit_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::is_space` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::is_ws` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::lower_fold` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_hash_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_hi_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_hi_put` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_len_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_lo_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_lo_put` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_mark_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_mark_put` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_off_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_path_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_path_set` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::module_name_bounds` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::name_eq` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::next_module_region` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::table_find` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::ws_trim_bounds` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::bits` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::contains` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::copy_on_write` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::empty` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::execute` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::is_empty` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::none` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::read` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::union` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::write` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::address_to_module` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::close_enumeration` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::get_all_virtual_pages` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::get_max_usermode_address` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::get_maximum_address` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::get_min_usermode_address` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::is_address_writable` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::next_module` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::next_virtual_page` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::open_modules` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::open_virtual_pages` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::resolve_module` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_queryer_trait::resolve_module_address` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_type_enum::MemoryTypeEnum::bits` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_type_enum::MemoryTypeEnum::contains` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_type_enum::MemoryTypeEnum::empty` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_type_enum::MemoryTypeEnum::image` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_type_enum::MemoryTypeEnum::is_empty` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_type_enum::MemoryTypeEnum::mapped` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_type_enum::MemoryTypeEnum::none` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_type_enum::MemoryTypeEnum::private` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::memory_type_enum::MemoryTypeEnum::union` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::byte_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::contains_address` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::get_base_address` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::get_end_address` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::get_module_address_display` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::get_module_name_len` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::get_region_size` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::new` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::new_with_display` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::set_base_address` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::set_module_address_display` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::set_module_name` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_queryer::normalized_module::NormalizedModule::set_region_size` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_reader::memory_reader_trait::read_bytes` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::memory_writer::memory_writer_trait::write_bytes` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::proc_paths::ProcName::for_pid` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::proc_paths::ProcName::for_process` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::proc_paths::ProcName::put_leaf` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::proc_paths::ProcName::put_pid` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::proc_paths::ProcName::reverse` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process::process_manager::ProcessManager::clear_opened_process` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process::process_manager::ProcessManager::get_opened_process` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process::process_manager::ProcessManager::set_opened_process` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::byte_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::c_name_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::c_name_set` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::collect_socket_snapshot` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::conn_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::conn_set` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::dec_token` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::dir_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::disp_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::disp_set` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::emit_into` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::has_display_env` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::inode_in_conn` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::inode_in_disp` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::io_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::is_windowed` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::lowered` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::name_matches` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::needle_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::needle_put` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::path_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::path_push` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::path_put_pid` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::path_reset` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::path_set` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::pid_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::pid_set` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::read_process_name` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::rec_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::rec_has_prefix` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::rec_set` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::stat_at` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::stream_next` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::token_has` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-engine-targets-native | `src::process_query::linux::linux_process_query::LinuxProcessQuery::unix_record` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-tests | `src::command_driver::CommandDriver::do_element_scan` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-tests | `src::command_driver::CommandDriver::do_scan_new` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-tests | `src::command_driver::CommandDriver::element_command` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-tests | `src::command_driver::CommandDriver::fail_geometry` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-tests | `src::command_driver::CommandDriver::init` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-tests | `src::command_driver::CommandDriver::list_command` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-tests | `src::command_driver::CommandDriver::new_command` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-tests | `src::command_driver::CommandDriver::run` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |
| squalr-tests | `src::command_driver::CommandDriver::verify_page` | DEPCHECK | DEPCHECK:targets-native-check (z4 in-flight fix) — cannot check inspection project: checked compilation failed for package `squalr-engine-targets-native` with 56 |

## Next gates (non-verifying machines grouped by diagnostic class)

| diagnostic class | machines | suggested leaf |
|---|---|---|
| DEPCHECK:targets-native-check (z4 in-flight fix) | 207 | `leaf/terminal-depcheck-targets-native-check` |

- `src::cli::Cli::init`
- `src::cli::Cli::is_exit_line`
- `src::cli::Cli::token_is_ci`
- `src::cli::Cli::to_upper`
- `src::cli::Cli::dec_places`
- `src::cli::Cli::run`
- `src::command_executors::collect_values_request_executor::CollectValuesRequestExecutor::execute`
- `src::command_executors::constraint_deanonymizer::ConstraintDeanonymizer::build_type_plan_list`
- `src::command_executors::element_scan_dispatcher::ElementScanChainDispatcher::dispatch_collection`
- `src::command_executors::element_scan_dispatcher::ElementScanChainDispatcher::run_chain`
- `src::command_executors::element_scan_dispatcher::ElementScanChainDispatcher::apply_plan`
- `src::command_executors::element_scan_dispatcher::ElementScanChainDispatcher::append_filters`
- `src::command_executors::element_scan_request_executor::ElementScanRequestExecutor::execute`
- `src::command_executors::element_scanner::ElementScannerDriver::scan_snapshot`
- `src::command_executors::element_scanner::ElementScannerDriver::scan_regions`
- `src::command_executors::element_scanner::ElementScannerDriver::dispatch_region`
- `src::command_executors::element_scanner::ElementScannerDriver::collect_metadata`
- `src::command_executors::privileged_command_executor::PrivilegedCommandExecutor::execute`
- `src::command_executors::scan_command_executor::ScanCommandExecutor::execute`
- `src::command_executors::scan_new_request_executor::ScanNewRequestExecutor::execute`
- `src::command_executors::scan_reset_request_executor::ScanResetRequestExecutor::execute`
- `src::command_executors::scan_results_command_executor::ScanResultsCommandExecutor::execute`
- `src::command_executors::scan_results_list_request_executor::ScanResultsListRequestExecutor::execute`
- `src::command_executors::scan_results_list_request_executor::ScanResultsListRequestExecutor::count_results`
- `src::command_executors::scan_results_list_request_executor::ScanResultsListRequestExecutor::enumerate_all`
- `src::command_executors::scan_results_list_request_executor::ScanResultsListRequestExecutor::merge_sorted`
- `src::command_executors::scan_results_list_request_executor::ScanResultsListRequestExecutor::count_by_type`
- `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::new`
- `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::get_region_count`
- `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::add_memory_region`
- `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::get_region`
- `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::fill_from_supplied_source`
- `src::command_executors::snapshot_region_builder::SnapshotRegionBuilder::fill_snapshot`
- `src::command_executors::snapshot_value_collector::SnapshotValueCollector::collect_all_regions`
- `src::squalr_engine::SqualrEngine::init`
- `src::squalr_engine::SqualrEngine::init_privileged_shell`
- `src::squalr_engine::SqualrEngine::new`
- `src::squalr_engine::SqualrEngine::get_mode`
- `src::squalr_engine::SqualrEngine::open_process`
- `src::squalr_engine::SqualrEngine::supply_memory`
- `src::squalr_engine::SqualrEngine::supply_fixture`
- `src::squalr_engine::SqualrEngine::dispatch_command`
- `src::engine_privileged_state::EnginePrivilegedState::init`
- `src::engine_privileged_state::EnginePrivilegedState::new`
- `src::engine_privileged_state::EnginePrivilegedState::has_opened_process`
- `src::engine_privileged_state::EnginePrivilegedState::get_opened_process`
- `src::engine_privileged_state::EnginePrivilegedState::set_opened_process`
- `src::engine_privileged_state::EnginePrivilegedState::make_fixture_source`
- `src::engine_privileged_state::EnginePrivilegedState::clear_opened_process`
- `src::engine_privileged_state::EnginePrivilegedState::get_snapshot`
- `src::engine_privileged_state::EnginePrivilegedState::borrow_snapshot`
- `src::engine_privileged_state::EnginePrivilegedState::borrow_snapshot_mut`
- `src::engine_privileged_state::EnginePrivilegedState::set_snapshot`
- `src::engine_privileged_state::EnginePrivilegedState::get_scan_settings`
- `src::engine_privileged_state::EnginePrivilegedState::get_scan_settings_ref`
- `src::engine_privileged_state::EnginePrivilegedState::set_scan_settings`
- `src::engine_privileged_state::EnginePrivilegedState::get_supplied_memory_source`
- `src::engine_privileged_state::EnginePrivilegedState::borrow_supplied_memory_source_mut`
- `src::engine_privileged_state::EnginePrivilegedState::get_freeze_list_count`
- `src::engine_privileged_state::EnginePrivilegedState::clear_freeze_list`
- `src::engine_privileged_state::EnginePrivilegedState::set_supplied_memory_source`
- `src::os::supplied_memory_source::SuppliedRegion::new`
- `src::os::supplied_memory_source::SuppliedRegion::get_base_address`
- `src::os::supplied_memory_source::SuppliedRegion::of_window`
- `src::os::supplied_memory_source::SuppliedRegion::get_region_size`
- `src::os::supplied_memory_source::SuppliedRegion::get_elements`
- `src::os::supplied_memory_source::SuppliedMemorySource::empty`
- `src::os::supplied_memory_source::SuppliedMemorySource::of_region`
- `src::os::supplied_memory_source::SuppliedMemorySource::get_region_count`
- `src::os::supplied_memory_source::SuppliedMemorySource::push_region`
- `src::os::supplied_memory_source::SuppliedRegion::clone_from`
- `src::os::supplied_memory_source::SuppliedRegion::clone`
- `src::os::supplied_memory_source::SuppliedMemorySource::get_page_bounds`
- `src::os::supplied_memory_source::SuppliedMemorySource::read_window`
- `src::os::supplied_memory_source::SuppliedMemorySource::read_u64`
- `src::os::supplied_memory_source::SuppliedMemorySource::clone_from`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::consume_line_position`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::buf_byte_at`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::hex_digit_at`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::acquire_maps`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::emit_min`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::module_name_bounds`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::ws_trim_bounds`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::is_ws`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::fill_module`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::next_module_region`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::base_in_modules`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::canon_path`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::hash_path`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::table_find`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::name_eq`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::is_space`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::lower_fold`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_lo_at`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_hi_at`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_off_at`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_len_at`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_hash_at`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_mark_at`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_mark_put`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_lo_put`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_hi_put`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_path_at`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::mod_path_set`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::canon_at`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::canon_set`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::buf_put`
- `src::memory_queryer::linux::linux_memory_queryer::LinuxMemoryQueryer::byte_at`
- `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::empty`
- `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::none`
- `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::read`
- `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::write`
- `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::execute`
- `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::copy_on_write`
- `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::contains`
- `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::union`
- `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::bits`
- `src::memory_queryer::memory_protection_enum::MemoryProtectionEnum::is_empty`
- `src::memory_queryer::memory_queryer_trait::open_virtual_pages`
- `src::memory_queryer::memory_queryer_trait::next_virtual_page`
- `src::memory_queryer::memory_queryer_trait::close_enumeration`
- `src::memory_queryer::memory_queryer_trait::get_all_virtual_pages`
- `src::memory_queryer::memory_queryer_trait::is_address_writable`
- `src::memory_queryer::memory_queryer_trait::get_maximum_address`
- `src::memory_queryer::memory_queryer_trait::get_min_usermode_address`
- `src::memory_queryer::memory_queryer_trait::get_max_usermode_address`
- `src::memory_queryer::memory_queryer_trait::open_modules`
- `src::memory_queryer::memory_queryer_trait::next_module`
- `src::memory_queryer::memory_queryer_trait::resolve_module`
- `src::memory_queryer::memory_queryer_trait::resolve_module_address`
- `src::memory_queryer::memory_queryer_trait::address_to_module`
- `src::memory_queryer::memory_type_enum::MemoryTypeEnum::empty`
- `src::memory_queryer::memory_type_enum::MemoryTypeEnum::none`
- `src::memory_queryer::memory_type_enum::MemoryTypeEnum::private`
- `src::memory_queryer::memory_type_enum::MemoryTypeEnum::image`
- `src::memory_queryer::memory_type_enum::MemoryTypeEnum::mapped`
- `src::memory_queryer::memory_type_enum::MemoryTypeEnum::contains`
- `src::memory_queryer::memory_type_enum::MemoryTypeEnum::union`
- `src::memory_queryer::memory_type_enum::MemoryTypeEnum::bits`
- `src::memory_queryer::memory_type_enum::MemoryTypeEnum::is_empty`
- `src::memory_queryer::normalized_module::NormalizedModule::new`
- `src::memory_queryer::normalized_module::NormalizedModule::new_with_display`
- `src::memory_queryer::normalized_module::NormalizedModule::byte_at`
- `src::memory_queryer::normalized_module::NormalizedModule::set_module_name`
- `src::memory_queryer::normalized_module::NormalizedModule::get_module_name_len`
- `src::memory_queryer::normalized_module::NormalizedModule::get_base_address`
- `src::memory_queryer::normalized_module::NormalizedModule::set_base_address`
- `src::memory_queryer::normalized_module::NormalizedModule::get_region_size`
- `src::memory_queryer::normalized_module::NormalizedModule::set_region_size`
- `src::memory_queryer::normalized_module::NormalizedModule::get_end_address`
- `src::memory_queryer::normalized_module::NormalizedModule::contains_address`
- `src::memory_queryer::normalized_module::NormalizedModule::get_module_address_display`
- `src::memory_queryer::normalized_module::NormalizedModule::set_module_address_display`
- `src::memory_reader::memory_reader_trait::read_bytes`
- `src::memory_writer::memory_writer_trait::write_bytes`
- `src::proc_paths::ProcName::for_process`
- `src::proc_paths::ProcName::for_pid`
- `src::proc_paths::ProcName::put_pid`
- `src::proc_paths::ProcName::reverse`
- `src::proc_paths::ProcName::put_leaf`
- `src::process::process_manager::ProcessManager::set_opened_process`
- `src::process::process_manager::ProcessManager::clear_opened_process`
- `src::process::process_manager::ProcessManager::get_opened_process`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::collect_socket_snapshot`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::unix_record`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::stream_next`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::rec_has_prefix`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::token_has`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::dec_token`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::inode_in_disp`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::inode_in_conn`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::read_process_name`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::name_matches`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::lowered`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::is_windowed`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::has_display_env`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::path_reset`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::path_put_pid`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::path_push`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::dir_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::io_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::stat_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::rec_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::rec_set`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::c_name_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::c_name_set`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::needle_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::needle_put`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::path_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::path_set`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::pid_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::pid_set`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::disp_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::disp_set`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::conn_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::conn_set`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::byte_at`
- `src::process_query::linux::linux_process_query::LinuxProcessQuery::emit_into`
- `src::command_driver::CommandDriver::init`
- `src::command_driver::CommandDriver::fail_geometry`
- `src::command_driver::CommandDriver::run`
- `src::command_driver::CommandDriver::new_command`
- `src::command_driver::CommandDriver::element_command`
- `src::command_driver::CommandDriver::list_command`
- `src::command_driver::CommandDriver::do_scan_new`
- `src::command_driver::CommandDriver::do_element_scan`
- `src::command_driver::CommandDriver::verify_page`

| InvalidUnitMachinePlan @ local construction stopped at state graph: result signature | 95 | `leaf/terminal-result-signature` |

- `src::commands::command_line::command_line_parser::CommandLineParser::parse`
- `src::commands::scan::element_scan::element_scan_request::ScanConstraintSet::push`
- `src::commands::scan_results::list::scan_results_list_response::ScanResultPage::push`
- `src::commands::scan_results::list::scan_results_list_response::ScanResultsListResponse::get_result_address`
- `src::commands::scan_results::scan_results_response::ScanResultsResponse::get_result_count`
- `src::conversions::storage_size_conversions::StorageSizeConversions::value_to_binary_size`
- `src::structures::data_types::data_type_ref::DataTypeRef::get_base_data_type_id_len`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::from_str`
- `src::structures::data_values::anonymous_value_string_format::AnonymousValueStringFormat::from_str_window`
- `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::from_str`
- `src::structures::memory::endian::Endian::equals`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_tail_links`
- `src::structures::pointer_scans::pointer_scan_address_space::PointerScanAddressSpace::from_str`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::new`
- `src::structures::results::snapshot_region_scan_results::PageElementList::push`
- `src::structures::results::snapshot_region_scan_results::PageElementList::insert_sorted`
- `src::structures::scan_results::scan_result::ScanResult::get_address`
- `src::structures::scanning::comparisons::scan_compare_type::ScanCompareType::from_str`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::covered_in_range`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::push_filter`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_filter_maximum_address`
- `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::push`
- `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::push_type_plans`
- `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_plan_list`
- `src::structures::snapshots::snapshot::Snapshot::push_region`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::push_page_boundary`
- `src::structures::snapshots::snapshot_region::DataTypeRefSet::push`
- `src::commands::scan_results::list::scan_results_list_response::ScanResultsListResponse::get_result_value`
- `src::commands::scan_results::scan_results_response::ScanResultsResponse::get_result_address`
- `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::parse_consistent`
- `src::conversions::storage_size_conversions::StorageSizeConversions::matches`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::copy_anonymous_value_string`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::parse`
- `src::structures::data_values::container_type::ContainerType::from_str`
- `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::from_str_window`
- `src::structures::memory::memory_alignment::AlignmentParseResult::parsed_size`
- `src::structures::memory::pointer::Pointer::get_root_display_text`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::display_text`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::contains_static_candidate`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_module_display_text`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::push_collection`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::get_number_of_results_for_data_types`
- `src::structures::results::snapshot_region_scan_results::MergeCursors::unfinished`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::is_data_type_in_set`
- `src::structures::scan_results::scan_result::ScanResult::get_current_value`
- `src::structures::scanning::comparisons::scan_compare_type::ScanCompareTypeParseResult::variant_probe`
- `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::parse`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_number_of_results`
- `src::structures::scanning::memory_read_mode::MemoryReadMode::from_str`
- `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::clone_data_type_refs`
- `src::structures::snapshots::element_window::ElementWindow::slice`
- `src::structures::snapshots::snapshot_region::DataTypeRefSet::get`
- `src::commands::scan::element_scan::element_scan_request::ScanConstraintSet::get`
- `src::commands::scan_results::list::scan_results_list_response::ScanResultPage::get`
- `src::commands::scan_results::scan_results_response::ScanResultsResponse::get_result_value`
- `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::parse`
- `src::conversions::storage_size_conversions::StorageSizeConversions::value_to_metric_size`
- `src::structures::data_types::data_type_ref::DataTypeRef::equals`
- `src::structures::data_types::data_type_ref::DataTypeRef::id_is`
- `src::structures::data_values::anonymous_value_string_format::AnonymousValueStringFormat::from_str`
- `src::structures::data_values::container_type::ContainerType::from_str_window`
- `src::structures::memory::memory_alignment::MemoryAlignment::from_str`
- `src::structures::memory::pointer::Pointer::get_offsets`
- `src::structures::memory::pointer::Pointer::has_symbolic_offsets`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::new_symbol`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::has_symbolic_links`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::new`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::get_number_of_results`
- `src::structures::results::snapshot_region_scan_results::PageElementList::get_page_element`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::enumerate_page`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_filter`
- `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::get_plan`
- `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_data_type_ref`
- `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_plan_list_for`
- `src::structures::snapshots::element_window::ElementWindow::push_element`
- `src::structures::snapshots::snapshot::Snapshot::get_region`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::covered_by_filters`
- `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_24_le`
- `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_24_be`
- `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_32_le`
- `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_32_be`
- `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_64_le`
- `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_unsigned_64_be`
- `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeSet::from_target_addresses`
- `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeSet::from_sorted_target_addresses`
- `src::scanners::element_scan_dispatcher::ElementScanDispatcher::dispatch_scalar_region`
- `src::scanners::element_scan_dispatcher::ScalarRegionScan::next`
- `src::scanners::element_scan_runner::ElementScanRunner::run_region`
- `src::scanners::scalar::scanner_scalar_iterative::ScalarIterativeScan::next`
- `src::scanners::scalar::scanner_scalar_single_element::ScannerScalarSingleElement::scan_region`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::is_prefix`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::suffix_length`
- `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::finalize_current_encode`
- `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::finalize_current_encode_with_padding`
- `src::scanners::structures::snapshot_region_filter_run_length_encoder::SnapshotRegionFilterRunLengthEncoder::finalize_current_encode_with_minimum_size_filtering`

| InvalidUnitMachinePlan @ local construction stopped at statement sequence: unsupported statement kind | 90 | `leaf/terminal-unsupported-statement-kind` |

- `src::commands::privileged_command_response::PrivilegedCommandResponse::is_scan`
- `src::commands::privileged_command_response::PrivilegedCommandResponse::get_result_address`
- `src::commands::scan::element_scan::element_scan_request::ScanConstraintSet::empty`
- `src::commands::scan_results::list::scan_results_list_response::ScanResultPage::empty`
- `src::conversions::storage_size_conversions::StorageSizeConversions::format_rounded`
- `src::structures::data_types::data_type_ref::DataTypeRef::parse`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::new_window`
- `src::structures::data_values::container_type::ContainerType::get_pointer_size`
- `src::structures::data_values::container_type::ContainerType::with_fixed_element_count`
- `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::all`
- `src::structures::memory::normalized_module::NormalizedModule::new_with_display`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::get_symbol_name`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_pointer_size`
- `src::structures::pointer_scans::pointer_scan_candidate::PointerScanCandidate::get_pointer_scan_node_type`
- `src::structures::processes::process_info::ProcessInfo::new_named`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::empty`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::get_result_counts_by_data_type`
- `src::structures::results::snapshot_region_scan_results::DataTypeResultCounts::get`
- `src::structures::results::snapshot_region_scan_results::PageElementList::clone`
- `src::structures::scan_results::scan_result::ScanResult::clone`
- `src::structures::scan_results::scan_result_base::ScanResultBase::get_data_type_ref`
- `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::new`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_memory_alignment`
- `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::new`
- `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::get_memory_alignment`
- `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::default`
- `src::structures::settings::scan_settings::ScanSettings::get_memory_alignment`
- `src::structures::snapshots::element_window::ElementWindow::empty`
- `src::structures::snapshots::snapshot::Snapshot::new`
- `src::structures::snapshots::snapshot::Snapshot::clone`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::get_scan_results`
- `src::commands::privileged_command_response::PrivilegedCommandResponse::is_scan_results`
- `src::commands::privileged_command_response::PrivilegedCommandResponse::get_result_value`
- `src::commands::scan::scan_response::ScanResponse::is_new`
- `src::commands::scan_results::list::scan_results_list_response::ScanResultsListResponse::default`
- `src::structures::data_types::data_type_ref::DataTypeRef::new`
- `src::structures::data_types::data_type_ref::DataTypeRef::clone`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::new`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::get_container_type`
- `src::structures::memory::normalized_module::NormalizedModule::new_from_normalized_region`
- `src::structures::processes::opened_process_info::OpenedProcessInfo::new`
- `src::structures::processes::opened_process_info::OpenedProcessInfo::get_target_architecture`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::clone`
- `src::structures::results::snapshot_region_scan_results::PageElementList::empty`
- `src::structures::results::snapshot_region_scan_results::DataTypeResultCounts::empty`
- `src::structures::scan_results::scan_result_data_type_count::ScanResultDataTypeCount::default`
- `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::get_scan_compare_type`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::new_with_result_size`
- `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::clone`
- `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_memory_alignment`
- `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::get_scan_compare_type`
- `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::get_planned_scan_type`
- `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::clone`
- `src::structures::settings::scan_settings::ScanSettings::get_memory_read_mode`
- `src::structures::snapshots::element_window::ElementWindow::of_length`
- `src::structures::snapshots::snapshot_region::DataTypeRefSet::empty`
- `src::commands::privileged_command_response::PrivilegedCommandResponse::get_result_count`
- `src::commands::scan::scan_response::ScanResponse::is_element_scan`
- `src::commands::scan_results::scan_results_response::ScanResultsResponse::is_list`
- `src::conversions::storage_size_conversions::StorageSizeConversions::zero_b`
- `src::structures::data_types::data_type_ref::DataTypeRef::default`
- `src::structures::data_types::data_type_ref::DataTypeRef::new_from_window`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::get_anonymous_value_string_format`
- `src::structures::data_values::container_type::ContainerType::from_pointer_size`
- `src::structures::memory::normalized_module::NormalizedModule::new`
- `src::structures::memory::normalized_module::NormalizedModule::new_from_normalized_region_with_display`
- `src::structures::memory::normalized_module::NormalizedModule::get_module_address_display`
- `src::structures::memory::pointer::Pointer::get_pointer_size`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::is_symbol`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_pointer_scan_node_type`
- `src::structures::processes::opened_process_info::OpenedProcessInfo::get_bitness`
- `src::structures::processes::process_info::ProcessInfo::new`
- `src::structures::results::snapshot_region_scan_results::MergeCursors::get_cursor`
- `src::structures::scan_results::scan_result::ScanResult::is_valued`
- `src::structures::scan_results::scan_result_base::ScanResultBase::new`
- `src::structures::scan_results::scan_result_data_type_count::ScanResultDataTypeCount::clone`
- `src::structures::scanning::comparisons::scan_compare_type::ScanCompareType::compare`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::empty`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_data_type_ref`
- `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::empty`
- `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::get_memory_read_mode`
- `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::get_scan_function_scalar`
- `src::structures::scanning::plans::pointer_scan::pointer_scan_execution_plan::PointerScanExecutionPlan::get_pointer_size`
- `src::structures::scanning::plans::pointer_scan::pointer_scan_execution_plan::PointerScanExecutionPlan::get_planned_kernel_kind`
- `src::structures::scanning::plans::pointer_scan::pointer_scan_parameters::PointerScanParameters::get_pointer_size`
- `src::structures::snapshots::element_window::ElementWindow::clone`
- `src::pointer_scans::search_kernels::pointer_scan_search_kernel_context::PointerScanSearchKernelContext::get_pointer_size`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::get_mismatch_shift`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::get_good_suffix_shift`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::mismatch_case`

| Unsupported: machine has no source-independent checked scalar control plan | 51 | `leaf/terminal-unsupported-machine-has-no-source-independent-checked-scalar` |

- `src::commands::command_line::command_line_parser::next_token`
- `src::commands::command_line::command_line_parser::flag_is`
- `src::structures::data_values::anonymous_value_string::holds`
- `src::structures::data_values::anonymous_value_string_format::refused`
- `src::structures::data_values::container_type::trim_right`
- `src::structures::data_values::container_type::index_of`
- `src::structures::data_values::pointer_scan_pointer_size::trim_right`
- `src::structures::data_values::pointer_scan_pointer_size::size_of`
- `src::structures::memory::address_display::write_hex_upper`
- `src::structures::memory::pointer_chain_segment::offsets_to_pointer_chain_segments`
- `src::structures::memory::symbolic_pointer_chain::copy_symbol_text`
- `src::structures::memory::symbolic_pointer_chain::write_prefixed_hex`
- `src::structures::memory::symbolic_pointer_chain::symbolic_pointer_chain_parse_offset`
- `src::structures::tasks::trackable_task::copy_task_text`
- `src::commands::command_line::command_line_parser::skip_space`
- `src::commands::command_line::command_line_parser::token_is`
- `src::commands::command_line::command_line_parser::flag_value`
- `src::commands::command_line::command_line_parser::parse_scan`
- `src::structures::data_values::anonymous_value_string_format::matches`
- `src::structures::data_values::container_type::total`
- `src::structures::data_values::pointer_scan_pointer_size::refused`
- `src::structures::memory::address_display::write_hex_upper_at`
- `src::structures::memory::address_display::format_module_address`
- `src::structures::memory::address_display::parse_gba_slot`
- `src::structures::pointer_scans::pointer_scan_address_space::ascii_eq`
- `src::structures::pointer_scans::pointer_scan_level_candidates::shift_static_insert`
- `src::commands::command_line::command_line_parser::token_end`
- `src::commands::command_line::command_line_parser::find_equals`
- `src::commands::command_line::command_line_parser::parse_u64`
- `src::commands::command_line::command_line_parser::parse_scan_results`
- `src::structures::data_values::anonymous_value_string_format::spelled`
- `src::structures::data_values::container_type::trim_left`
- `src::structures::data_values::container_type::parse_u64_window`
- `src::structures::data_values::pointer_scan_pointer_size::trim_left`
- `src::structures::data_values::pointer_scan_pointer_size::matches_lower`
- `src::structures::memory::address_display::format_absolute_address`
- `src::structures::memory::address_display::ascii_eq_fold`
- `src::structures::memory::address_display::try_resolve_virtual_module_address`
- `src::structures::memory::pointer::copy_text`
- `src::structures::memory::symbolic_pointer_chain::symbolic_pointer_chain_format_offset`
- `src::structures::memory::symbolic_pointer_chain::symbolic_pointer_chain_is_valid_symbol_name`
- `src::structures::pointer_scans::pointer_scan_level_candidates::shift_heap_insert`
- `src::structures::results::snapshot_region_scan_results::is_data_type_selected`
- `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_byte_at`
- `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_pointer_value_unchecked`
- `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_pointer_lane_values_u32`
- `src::pointer_scans::search_kernels::pointer_scan_pointer_value_reader::read_pointer_lane_values_u64`
- `src::pointer_scans::search_kernels::pointer_scan_scalar_region_scanner::scan_region_scalar_with_predicate`
- `src::pointer_scans::search_kernels::pointer_scan_search_kernel_utils::find_scan_start_offset`
- `src::pointer_scans::structures::pointer_scan_target_ranges::pointer_scan_target_range_set_contains_value_linear`
- `src::pointer_scans::structures::pointer_scan_target_ranges::pointer_scan_target_range_set_contains_value_binary`

| InvalidUnitMachinePlan @ local construction stopped at structural field store: scalar field type | 42 | `leaf/terminal-structural-field-store-scalar-field-type` |

- `src::conversions::storage_size_conversions::StorageSizeText::put_byte`
- `src::structures::data_types::data_type_ref::DataTypeRef::clone_from`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::clone_from`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::set_anonymous_value_string_format`
- `src::structures::memory::normalized_module::NormalizedModule::set_module_name`
- `src::structures::memory::pointer::Pointer::set_pointer_size`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::set_module_name`
- `src::structures::processes::opened_process_info::OpenedProcessInfo::with_target_architecture`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::set_filter_collection`
- `src::structures::results::snapshot_region_scan_results::MergeCursors::set_cursor`
- `src::structures::scan_results::scan_result_base::ScanResultBase::clone_from`
- `src::structures::scan_results::scan_result_data_type_count::ScanResultDataTypeCount::clone_from`
- `src::structures::scan_results::scan_result_valued::ScanResultValued::clone_from`
- `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::clone_from`
- `src::structures::scanning::plans::pointer_scan::pointer_scan_execution_plan::PointerScanExecutionPlan::set_planned_kernel_kind`
- `src::structures::snapshots::element_window::ElementWindow::clone_from`
- `src::structures::snapshots::element_window::ElementWindow::truncate_front`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::clone_from`
- `src::conversions::storage_size_conversions::StorageSizeText::put_digits_reversed`
- `src::conversions::storage_size_conversions::StorageSizeText::put_suffix`
- `src::structures::data_types::data_type_ref::DataTypeRef::copy_id_window`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::fill_value`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::copy_bytes`
- `src::structures::memory::pointer::Pointer::set_module_name`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::set_pointer_size`
- `src::structures::processes::process_info::ProcessInfo::set_name`
- `src::structures::results::snapshot_region_scan_results::PageElement::clone_from`
- `src::structures::scan_results::scan_result_base::ScanResultBase::copy_icon`
- `src::structures::snapshots::element_window::ElementWindow::copy_from`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::copy_boundaries`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::set_current_values`
- `src::conversions::storage_size_conversions::StorageSizeText::reverse`
- `src::structures::data_types::data_type_ref::DataTypeRef::set_data_type_id`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::set_anonymous_value_string`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::set_container_type`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::set_module_name`
- `src::structures::processes::opened_process_info::OpenedProcessInfo::set_name`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::clone_from`
- `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::set_planned_scan_type`
- `src::structures::scanning::plans::element_scan::snapshot_filter_element_scan_plan::SnapshotFilterElementScanPlan::clone_from`
- `src::structures::snapshots::element_window::ElementWindow::set_element`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::rotate_values_for_collection`

| InvalidUnitMachinePlan @ local construction stopped at result type | 40 | `leaf/terminal-result-type` |

- `src::conversions::storage_size_conversions::StorageSizeConversions::metric_suffix`
- `src::structures::data_values::anonymous_value_string_format::AnonymousValueStringFormat::spelling`
- `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::spelling`
- `src::structures::memory::pointer::Pointer::new`
- `src::structures::memory::pointer::Pointer::get_offset_segments`
- `src::structures::memory::pointer::Pointer::get_module_name`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::new`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_links`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_static_candidates`
- `src::structures::scanning::plans::pointer_scan::planned_pointer_scan_kernel_kind::PlannedPointerScanKernelKind::get_display_name`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::get_current_values_slice`
- `src::conversions::storage_size_conversions::StorageSizeConversions::binary_suffix`
- `src::structures::memory::normalized_module::NormalizedModule::get_module_name`
- `src::structures::memory::pointer::Pointer::new_with_size`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::new_absolute`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_module_name`
- `src::structures::pointer_scans::pointer_scan_address_space::PointerScanAddressSpace::get_label`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::new_presorted`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::new_materialized`
- `src::structures::scanning::rules::pointer_scan::built_in_planning_rules::rule_map_search_kernel::RuleMapSearchKernel::rule_id`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::get_previous_values_slice`
- `src::structures::tasks::trackable_task::TrackableTask::create`
- `src::structures::memory::pointer::Pointer::new_with_size_and_segments`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::new_allow_empty`
- `src::structures::pointer_scans::pointer_scan_address_space::PointerScanAddressSpace::get_display_name`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_heap_candidates`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::new`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_module_name`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_child_node_ids`
- `src::structures::scanning::rules::pointer_scan::built_in_planning_rules::rule_map_search_kernel::RuleMapSearchKernel::get_id`
- `src::structures::tasks::trackable_task::TrackableTask::get_task_handle`
- `src::structures::tasks::trackable_task::TrackableTask::get_name`
- `src::structures::tasks::trackable_task::TrackableTask::get_task_identifier`
- `src::structures::tasks::trackable_task_handle::TrackableTaskHandle::clone`
- `src::pointer_scans::search_kernels::pointer_scan_search_kernel_context::PointerScanSearchKernelContext::new`
- `src::pointer_scans::search_kernels::pointer_scan_search_kernel_context::PointerScanSearchKernelContext::get_target_range_set`
- `src::pointer_scans::structures::pointer_scan_collected_level::PointerScanCollectedLevel::new`
- `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeSet::empty`
- `src::pointer_scans::structures::snapshot_region_scan_task::SnapshotRegionScanTasks::new`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::new`

| Unsupported: borrowed slice view has no Terminal descriptor | 33 | `leaf/terminal-unsupported-borrowed-slice-view-has-no-terminal-descriptor` |

- `src::structures::memory::pointer::Pointer::get_address`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_node_count`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_graph_node_id`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::has_parent_node_id`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_depth`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::set_branch_total_depth`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_resolved_target_address`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_module_offset`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::has_children`
- `src::structures::memory::pointer::Pointer::set_address`
- `src::structures::memory::pointer::Pointer::get_offset_count`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_link_count`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_static_node_count`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_discovery_depth`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_parent_node_id`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::set_depth`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_pointer_address`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_pointer_offset`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::is_empty`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_discovery_depth`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::get_heap_node_count`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_node_id`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_branch_total_depth`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::set_discovery_depth`
- `src::structures::pointer_scans::pointer_scan_node::PointerScanNode::get_pointer_value`
- `src::pointer_scans::structures::pointer_scan_target_ranges::PointerScanTargetRangeSet::get_source_target_count`
- `src::pointer_scans::structures::pointer_scan_target_ranges::pointer_scan_target_range_set_get_range_count`
- `src::pointer_scans::structures::pointer_scan_target_ranges::pointer_scan_target_range_set_is_empty`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::get_aligned_pattern_length`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::mismatch_absent`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::u64_min`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::u64_max`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::round_up_to_alignment`

| NOT_FOUND: trait-signature decls (no concrete machine name) | 17 | `leaf/terminal-not-found-trait-signature-decls` |

- `src::structures::scanning::rules::pointer_scan_planning_rule::map_plan`
- `src::structures::memory::normalized_region::equals`
- `src::structures::scanning::filters::snapshot_region_filter::equals`
- `src::structures::scanning::rules::pointer_scan_planning_rule::get_id`
- `src::pointer_scans::search_kernels::pointer_scan_simd_linear_search_kernel::visit`
- `src::target_providers::start_monitoring`
- `src::target_providers::stop_monitoring`
- `src::target_providers::get_processes`
- `src::target_providers::open_process`
- `src::target_providers::close_process`
- `src::target_providers::is_process_alive`
- `src::target_providers::open_page_bounds`
- `src::target_providers::next_page_bounds_region`
- `src::target_providers::close_page_bounds`
- `src::target_providers::is_address_writable`
- `src::target_providers::read_bytes`
- `src::target_providers::write_bytes`

| InvalidUnitMachinePlan @ local construction stopped at statement sequence: call: call operation | 15 | `leaf/terminal-call-call-operation` |

- `src::registries::scan_rules::pointer_scan_rule_registry::PointerScanRuleRegistry::map_pointer_scan_execution_plan`
- `src::structures::data_values::container_type::ContainerType::from_str_consistent`
- `src::structures::memory::memory_alignment::MemoryAlignment::from_str_consistent`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::copy_collections`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::advance_cursor`
- `src::structures::scanning::filters::snapshot_region_filter::SnapshotRegionFilter::clone_consistent`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::copy_filters`
- `src::structures::scanning::plans::element_scan::element_scan_plan::TypePlanList::clone_from`
- `src::structures::results::snapshot_region_scan_results::DataTypeResultCounts::fill`
- `src::structures::results::snapshot_region_scan_results::PageElementList::copy_from`
- `src::structures::results::snapshot_region_scan_results::PageElementList::shift_down`
- `src::structures::snapshots::snapshot::Snapshot::clone_from`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::from_str_consistent`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::clone_from`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::set_scan_results`

| InvalidUnitMachinePlan @ local construction stopped at outer calls: ordered statement call | 13 | `leaf/terminal-ordered-statement-call` |

- `src::structures::scan_results::scan_result_base::ScanResultBase::default`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::new`
- `src::structures::data_values::anonymous_value_string_format::AnonymousValueStringFormat::from_str_consistent`
- `src::structures::scan_results::scan_result_valued::ScanResultValued::default`
- `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::new_no_value`
- `src::conversions::storage_size_conversions::StorageSizeConversions::value_to_text_consistent`
- `src::structures::data_values::pointer_scan_pointer_size::PointerScanPointerSize::from_str_consistent`
- `src::structures::scan_results::scan_result::ScanResult::default`
- `src::structures::scanning::comparisons::scan_compare_type::ScanCompareType::from_str_consistent`
- `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::clone`
- `src::structures::scanning::plans::element_scan::element_scan_plan::ElementScanPlan::new`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::clone`
- `src::scanners::scalar::scanner_scalar_iterative::ScalarIterativeScan::new`

| InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: guard expression | 11 | `leaf/terminal-guard-expression` |

- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::ensure_minimum_links`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::ensure_heap_candidates_sorted`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::resize_to_filters`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::compute_filter_bounds`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_numeric_tail_offsets`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::from_str`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChain::get_numeric_root_offset`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::find_heap_candidates_in_range`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::initialize_scan_results`
- `src::pointer_scans::structures::pointer_scan_collected_level::PointerScanCollectedLevel::push_static`
- `src::pointer_scans::structures::pointer_scan_collected_level::PointerScanCollectedLevel::push_heap`

| InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a local initializer | 9 | `leaf/terminal-unconsumed-nested-call-in-a-local-initializer` |

- `src::structures::scanning::constraints::anonymous_scan_constraint::AnonymousScanConstraint::get_anonymous_value_string`
- `src::structures::scan_results::scan_result_valued::ScanResultValued::get_base_result`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::clone`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::get_collected_byte_count`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::clone`
- `src::structures::results::snapshot_region_scan_results::PageElement::clone`
- `src::structures::scan_results::scan_result_base::ScanResultBase::clone`
- `src::structures::scan_results::scan_result_valued::ScanResultValued::clone`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::from_single_filter`

| Unsupported: Unit graph borrowed parameter is not a primitive or byte slice | 8 | `leaf/terminal-unsupported-unit-graph-borrowed-parameter-is-not-a-primitive` |

- `src::structures::memory::normalized_region::NormalizedRegion::clone`
- `src::structures::scan_results::scan_result_ref::ScanResultRef::clone`
- `src::structures::data_types::generics::vectorization_plan::VectorizationPlan::clone`
- `src::structures::scan_results::scan_result_base::ScanResultBase::get_handle`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::get_normalized_region`
- `src::structures::results::snapshot_region_scan_results::ResultCursor::clone`
- `src::structures::results::snapshot_region_scan_results::CursorProbe::smaller`
- `src::structures::scan_results::scan_results_metadata::ScanResultsMetadata::clone`

| InvalidUnitMachinePlan @ local construction stopped at signature | 8 | `leaf/terminal-signature` |

- `src::structures::tasks::trackable_task::TrackableTask::get_progress`
- `src::structures::tasks::trackable_task::TrackableTask::set_name`
- `src::structures::tasks::trackable_task::TrackableTask::get_cancellation_token`
- `src::structures::tasks::trackable_task::TrackableTask::complete`
- `src::structures::tasks::trackable_task::TrackableTask::set_task_identifier`
- `src::structures::tasks::trackable_task::TrackableTask::is_completed`
- `src::structures::tasks::trackable_task::TrackableTask::subscribe_to_progress_updates`
- `src::structures::tasks::trackable_task::TrackableTask::cancel`

| Unsupported: scalar computation needs one checked expression and one source binding | 7 | `leaf/terminal-unsupported-scalar-computation-needs-one-checked-expression-a` |

- `src::structures::snapshots::snapshot_region::SnapshotRegion::get_previous_element`
- `src::structures::data_types::data_type_ref::DataTypeRef::get_unit_size_in_bytes`
- `src::structures::snapshots::element_window::ElementWindow::get_element`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::get_current_element`
- `src::structures::snapshots::snapshot::Snapshot::get_collected_byte_count`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::has_current_values`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::get_page_boundary`

| InvalidTerminalModule | 6 | `leaf/terminal-invalidterminalmodule` |

- `src::structures::results::snapshot_region_scan_results::PageElement::of`
- `src::structures::scan_results::scan_result_data_type_count::ScanResultDataTypeCount::new`
- `src::structures::scan_results::scan_result_valued::ScanResultValued::new`
- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::new_offset`
- `src::structures::settings::scan_settings::ScanSettings::default`
- `src::process_query::process_query_options::ProcessQueryOptions::default`

| InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: target state | 6 | `leaf/terminal-target-state` |

- `src::structures::scanning::rules::pointer_scan::built_in_planning_rules::rule_map_search_kernel::RuleMapSearchKernel::map_plan`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::parse_u64`
- `src::structures::pointer_scans::pointer_scan_level_candidates::PointerScanLevelCandidates::find_heap_candidate_by_address`
- `src::structures::scanning::rules::pointer_scan::built_in_planning_rules::rule_map_search_kernel::RuleMapSearchKernel::select_kernel_kind`
- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::probe_cursor`
- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::locate_result`

| PANIC: boolean-short-circuit-lowering (checked-trees-to-lowered-psi boolean.rs:204 unreachable) | 4 | `leaf/terminal-panic-boolean-short-circuit-lowering` |

- `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::is_ascii_hexdigit`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::pick_min`
- `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::uppercase_ascii`
- `src::structures::snapshots::snapshot_region::SnapshotRegion::pick_max`

| InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: conditional successors: edge cleanup | 4 | `leaf/terminal-edge-cleanup` |

- `src::structures::snapshots::snapshot::Snapshot::set_region`
- `src::structures::snapshots::snapshot::Snapshot::initialize_all_scan_results`
- `src::structures::snapshots::snapshot::Snapshot::apply_region_scan_results`
- `src::structures::snapshots::snapshot::Snapshot::collect_region_values`

| InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter signature: attached data shape | 4 | `leaf/terminal-state-signature-parameter-signature-attached-data-shape` |

- `src::structures::tasks::trackable_task::TrackableTask::next_progress_update`
- `src::structures::tasks::trackable_task::TrackableTask::set_progress`
- `src::structures::tasks::trackable_task::TrackableTask::wait_for_progress_update`
- `src::structures::tasks::trackable_task::TrackableTask::wait_for_completion`

| Unsupported: indexed reads require a whole byte-view parameter | 3 | `leaf/terminal-unsupported-indexed-reads-require-a-whole-byte-view-parameter` |

- `src::conversions::storage_size_conversions::StorageSizeText::get_byte`
- `src::structures::data_values::anonymous_value_string::AnonymousValueString::get_anonymous_value_string_byte`
- `src::structures::data_types::data_type_ref::DataTypeRef::get_data_type_id_byte`

| InvalidUnitMachinePlan @ local construction stopped at statement sequence: local data: scalar local: pure initializer | 3 | `leaf/terminal-local-data-scalar-local-pure-initializer` |

- `src::conversions::storage_size_conversions::StorageSizeConversions::binary_scale`
- `src::structures::data_types::generics::vector_generics::VectorGenerics::plan_vector_scan`
- `src::conversions::storage_size_conversions::StorageSizeConversions::metric_scale`

| InvalidUnitMachinePlan @ local construction stopped at statement sequence: structural result: returned value | 3 | `leaf/terminal-structural-result-returned-value` |

- `src::structures::pointer_scans::pointer_scan_candidate::PointerScanCandidate::new`
- `src::structures::scanning::plans::pointer_scan::pointer_scan_execution_plan::PointerScanExecutionPlan::new`
- `src::structures::scanning::plans::pointer_scan::pointer_scan_parameters::PointerScanParameters::new`

| InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a transition | 3 | `leaf/terminal-unconsumed-nested-call-in-a-transition` |

- `src::structures::data_values::container_type::ContainerType::get_total_size_in_bytes`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::get_safe_mismatch_shift`
- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::mismatch_present`

| InvalidUnitMachinePlan @ local construction stopped at statement sequence: local data: structural result shape | 3 | `leaf/terminal-local-data-structural-result-shape` |

- `src::pointer_scans::search_kernels::pointer_scan_scalar_binary_search_kernel::ScalarBinaryPointerScanKernel::is_empty`
- `src::pointer_scans::search_kernels::pointer_scan_scalar_linear_search_kernel::ScalarLinearPointerScanKernel::is_empty`
- `src::pointer_scans::search_kernels::pointer_scan_simd_linear_search_kernel::SimdLinearPointerScanKernel::is_empty`

| InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter signature: structural parameter type | 3 | `leaf/terminal-state-signature-parameter-signature-structural-parameter-type` |

- `src::pointer_scans::search_kernels::pointer_scan_scalar_binary_search_kernel::ScalarBinaryPointerScanKernel::scan_region_with_visitor`
- `src::pointer_scans::search_kernels::pointer_scan_scalar_linear_search_kernel::ScalarLinearPointerScanKernel::scan_region_with_visitor`
- `src::pointer_scans::search_kernels::pointer_scan_simd_linear_search_kernel::SimdLinearPointerScanKernel::scan_region_with_visitor`

| Unsupported: scalar graph control must be acyclic | 2 | `leaf/terminal-unsupported-scalar-graph-control-must-be-acyclic` |

- `src::structures::memory::address_display::offset_width`
- `src::structures::memory::symbolic_pointer_chain::hex_width`

| Unsupported: direct scalar call target has an unsupported terminal signature | 2 | `leaf/terminal-unsupported-direct-scalar-call-target-has-an-unsupported-term` |

- `src::conversions::storage_size_conversions::StorageSizeConversions::metric_place`
- `src::conversions::storage_size_conversions::StorageSizeConversions::binary_place`

| Unsupported: composed Unit attachment is not a record | 2 | `leaf/terminal-unsupported-composed-unit-attachment-is-not-a-record` |

- `src::structures::memory::symbolic_pointer_chain::SymbolicPointerChainLink::as_offset`
- `src::structures::processes::target_architecture::TargetArchitecture::get_pointer_width`

| InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: guarded jump successors: roster | 2 | `leaf/terminal-guarded-jump-successors-roster` |

- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::sort_filters`
- `src::scanners::element_scan_runner::ElementScanRunner::drain_iterative`

| InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter custody shape: borrowed non-view carrier | 2 | `leaf/terminal-state-signature-parameter-custody-shape-borrowed-non-view-car` |

- `src::structures::snapshots::snapshot::Snapshot::set_snapshot_regions`
- `src::structures::snapshots::snapshot::Snapshot::store_regions`

| Unsupported: scalar graph structural formals require whole parameter transfers | 1 | `leaf/terminal-unsupported-scalar-graph-structural-formals-require-whole-par` |

- `src::conversions::conversions_from_hex_pattern::ConversionsFromHexPattern::has_wildcards`

| Unsupported: signed wrapping conversion requires runtime policy realization | 1 | `leaf/terminal-unsupported-signed-wrapping-conversion-requires-runtime-polic` |

- `src::structures::memory::symbolic_pointer_chain::symbolic_pointer_chain_apply_pointer_offset`

| InvalidUnitMachinePlan @ local construction stopped at state graph: terminator: jump successor: parameter transfer | 1 | `leaf/terminal-jump-successor-parameter-transfer` |

- `src::structures::results::snapshot_region_scan_results::DataTypeResultCounts::merge_from`

| OperationProofUnavailable | 1 | `leaf/terminal-operationproofunavailable` |

- `src::structures::scanning::comparisons::scan_compare_type_delta::ScanCompareTypeDelta::compare`

| InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: parameter custody shape: owned non-linear unnamed type | 1 | `leaf/terminal-state-signature-parameter-custody-shape-owned-non-linear-unna` |

- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::retain_result_sized_filters`

| InvalidUnitMachinePlan @ local construction stopped at statement sequence: assignment: call source result type | 1 | `leaf/terminal-assignment-call-source-result-type` |

- `src::structures::scan_results::scan_result::ScanResult::clone_from`

| InvalidUnitMachinePlan @  | 1 | `leaf/terminal-unknown-stage` |

- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::set_filter`

| InvalidUnitMachinePlan @ local construction stopped at outer calls: unconsumed nested call in a call statement | 1 | `leaf/terminal-unconsumed-nested-call-in-a-call-statement` |

- `src::structures::snapshots::snapshot_region::SnapshotRegion::from_elements`

| InvalidUnitMachinePlan @ local construction stopped at outer calls: structural operands | 1 | `leaf/terminal-structural-operands` |

- `src::structures::results::snapshot_region_scan_results::SnapshotRegionScanResults::get_filter_collection`

| Unsupported: record operand has no named or projected source | 1 | `leaf/terminal-unsupported-record-operand-has-no-named-or-projected-source` |

- `src::structures::scanning::filters::snapshot_region_filter_collection::SnapshotRegionFilterCollection::get_filter_minimum_address`

| InvalidUnitMachinePlan @ local construction stopped at state graph: prefix initializers: bound expression | 1 | `leaf/terminal-prefix-initializers-bound-expression` |

- `src::structures::snapshots::snapshot::Snapshot::discard_empty_regions`

| InvalidUnitMachinePlan @ local construction stopped at state graph: state signature: contract shape unadmitted | 1 | `leaf/terminal-state-signature-contract-shape-unadmitted` |

- `src::scanners::structures::boyer_moore_table::BoyerMooreTable::build_table`

