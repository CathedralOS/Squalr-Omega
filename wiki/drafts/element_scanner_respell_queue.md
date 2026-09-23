# element_scanner.omg — owned-shape respell queue (merge/scalar-value-parsers)

Coordinator repair progress committed as 5099d0b on this lane. Remaining
diagnostics are design-level re-port items, not renames — the lane was written
against a stale api surface.

## Done (mechanical, committed)
- `DataTypeRef<'a>`/`<'t>` stripped in api + scanning files.
- `SnapshotRegionFilterCollection`, `ElementScanPlan`, `Snapshot`,
  `SnapshotRegion`, `SnapshotRegionScanResults` generic args stripped to
  main's non-generic owned shapes.
- `CollectionRef::{Found,Missing}` call site converted to owned
  `get_filter_collection` + `get_collection_count` bound guard.
- `regions: &'a mut [SnapshotRegion]` params/args dropped (dead forwarding;
  region access goes through `snapshot.get_region`/`set_region` clones).
- `snapshot.snapshot_regions` → `snapshot.regions`.
- `commit_deleted_scan_result_indices` → `0` (delete leg unported this pin).
- `get_data_type_refs()` → `clone_data_type_refs()` (owned `DataTypeRefSet`);
  `&'t [DataTypeRef]` params → owned `DataTypeRefSet`; indexed reads → `.get(i)`.
- `DataTypeRef::get_data_type_id() -> &[u8]` view getter ADDED to api
  (data_type_ref.omg) — keep it.
- `SnapshotRegionFilterCollection::new(view,…)` → `from_single_filter(&seed,…)`.

## Remaining — design-level (z2's queue)
38+ diagnostics at last count. Categories:
- **Missing api entirely** — needs upstream-semantic port, not rename:
  `element_scan_plan.count_constraints_for`/`constraint_index_for`/
  `get_constraint` (constraint navigation — api exposes
  `get_plan_list`/`get_plan_list_for` instead), `snapshot_region.
  has_previous_values`/`read_current_elements`,
  `collection.number_of_results` field (→ `get_number_of_results()`),
  `snapshot.get_byte_count` (→ `get_collected_byte_count`),
  `snapshot.get_number_of_results` (aggregate; api has per-region
  `get_number_of_results` / `get_number_of_results_for_data_types` —
  may need a loop or api addition).
- **`&mut`-through-param-field writes** — `snapshot.regions[i].set_scan_results`
  /`.discard_empty_regions` mint `argument self expects &mut Self, got named
  value`: must go get-clone → mutate → `set_region` writeback.
- **`initialize_scan_results` expects 3 args, got 2** — signature moved.
- **`new` expects 2 got 1** — `SnapshotRegionScanResults::new(view)` needs
  (array, count) both args.
- **`get_region` self-type error** — call `snapshot.get_region(i)` on
  `&mut Snapshot` param; receiver type mismatch needs `&` vs `&mut` care.

## Upstream semantics to preserve
One single-filter collection per data type (from_single_filter), region
clone-out/set-in writeback discipline, serial fallback of upstream
`par_iter_mut` fan-out. No placeholder bodies — AGENTS rule.
