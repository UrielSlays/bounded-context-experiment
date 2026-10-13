$ErrorActionPreference = 'Stop'

function Assert-True {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw $Message }
}

function Read-Json {
    param([string]$Name)
    $path = Join-Path $PSScriptRoot $Name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing normative artifact: $Name"
    }
    return Get-Content -LiteralPath $path -Raw | ConvertFrom-Json -Depth 100
}

$required = @(
    'MBCX-01-EXPERIMENT-DESIGN-r6.md',
    'MBCX-01-STATE-ACTION-CONTRACT-v2.json',
    'MBCX-01-PACKET-SCHEMAS-v1.json',
    'MBCX-01-MEASUREMENT-CONTRACT-v1.json',
    'MBCX-01-INFERENCE-CONTRACT-v2.json'
)
foreach ($name in $required) {
    Assert-True (Test-Path -LiteralPath (Join-Path $PSScriptRoot $name) -PathType Leaf) "Missing normative artifact: $name"
}

$state = Read-Json 'MBCX-01-STATE-ACTION-CONTRACT-v2.json'
$packets = Read-Json 'MBCX-01-PACKET-SCHEMAS-v1.json'
$measurement = Read-Json 'MBCX-01-MEASUREMENT-CONTRACT-v1.json'
$inference = Read-Json 'MBCX-01-INFERENCE-CONTRACT-v2.json'

Assert-True ($state.base_event.idempotency_identity -eq '(scope_id,semantic_operation,idempotency_key)') 'Cross-scope idempotency identity is not total.'
Assert-True ($state.serialization.integer_min -eq -9007199254740991) 'Safe integer minimum is not frozen.'
Assert-True ($state.serialization.integer_max -eq 9007199254740991) 'Safe integer maximum is not frozen.'
Assert-True ($state.action_executor.ACT_ON_OBLIGATION.transition -eq 'complete_obligation') 'ACT is not mapped to complete_obligation.'
Assert-True ($state.action_executor.ACT_ON_OBLIGATION.completion_action_source -eq 'obligation.completion_action_id') 'ACT incorrectly substitutes its public ID for completion_action_id.'
Assert-True ($state.writer.invalid_proposal_action -eq 'append reject_handoff_result exactly once') 'Invalid proposals retain divergent writer paths.'
Assert-True ($state.event_types.record_call_response.key -eq '(scenario_id,condition,node)') 'Accepted responses are not journaled for every node.'
Assert-True (($state.event_types.record_call_response.allowed_nodes -join ',') -eq 'A0,B,A1') 'A0/B/A1 response journal coverage is incomplete.'
Assert-True ($state.paid_handoff_gold.required_gold_cardinality -eq 1) 'Paid cuts still permit hidden multi-gold guessing.'
Assert-True ($state.packet_type_names.worker -eq 'WorkerHandoffV2') 'Worker handoff version remains inconsistent.'

foreach ($schemaName in @('DecisionPacketV2','TaskPacketV2','WorkerHandoffV2')) {
    $schema = $packets.schemas.$schemaName
    Assert-True ($null -ne $schema) "Missing schema: $schemaName"
    Assert-True ($schema.additionalProperties -eq $false) "$schemaName is not closed."
}
Assert-True ($packets.renderer.discriminator.kind -eq 'deterministic_unpaid') 'Render discriminator is not deterministic and unpaid.'
Assert-True ($packets.renderer.id_permutation_required -eq $true) 'ID-only render leakage is not tested.'
Assert-True ($packets.schemas.WorkerHandoffV2.properties.reasoning -eq $null) 'Worker handoff admits free-text reasoning.'

$units = @($measurement.counter_catalog | ForEach-Object unit_class | Sort-Object -Unique)
foreach ($unit in @('bytes','records','pages','operations','branches')) {
    Assert-True ($units -contains $unit) "Missing physical counter unit class: $unit"
    Assert-True ($null -ne $measurement.unit_class_total_gates.$unit) "Missing total-charge gate for: $unit"
}
Assert-True ($measurement.counter_set_closed -eq $true) 'Counter splitting remains possible through unregistered counters.'
Assert-True ($measurement.crossed_axes.H_at_D -contains 256) 'H is not crossed at high D.'
Assert-True ($measurement.crossed_axes.D_at_H -contains 100000) 'D is not crossed at high H.'
Assert-True ($measurement.red_candidates -contains 'HD_INTERACTION_ARCHIVE_LINEAR') 'H-by-D false-pass witness is missing.'
Assert-True ($measurement.candidate_config.additionalProperties -eq $false) 'Candidate config remains an open taint channel.'
Assert-True ($measurement.candidate_config.prohibited_fields -contains 'precomputed_packet') 'Precomputed-packet taint is not forbidden.'

Assert-True ($inference.estimands.delta -match 'average conditional mean') 'Delta estimand does not cover varying conditional means.'
Assert-True ($inference.method.name -eq 'three-look bounded-martingale Hoeffding intervals') 'Primary method is not the frozen varying-mean method.'
Assert-True ($inference.method.look_alpha -eq ($inference.method.stream_alpha / 3)) 'Look alpha is not Bonferroni-frozen.'
Assert-True ($inference.missingness.completion_space -eq '{00,01,10,11}^m') 'Joint BC/OM missingness is not enumerated.'
Assert-True ($inference.missingness.branch_invariance_required -eq $true) 'Missing OM can still choose a branch.'
Assert-True ($inference.reference_sources.predmix_py.git_blob -eq 'f7c3b4bf17411596d1434e3330796f3e8c8ff884') 'predmix.py Git blob is wrong.'
Assert-True ($inference.reference_sources.betting_strategies_py.git_blob -eq '89f433fd24274e7c74d7d93fe054399fb87cfaca') 'betting_strategies.py Git blob is wrong.'
Assert-True ($inference.reference_vectors.periodic_indexing -eq 'zero_based_indices_0_10_20') 'Periodic reference-vector indexing is not frozen.'

foreach ($cell in $inference.operating_characteristics.cells) {
    $p = @($cell.p00, $cell.p01, $cell.p10, $cell.p11)
    Assert-True (-not ($p | Where-Object { $_ -lt 0 })) "OC cell $($cell.id) has a negative probability."
    Assert-True ([Math]::Abs((($p | Measure-Object -Sum).Sum) - 1.0) -lt 1e-12) "OC cell $($cell.id) does not sum to one."
}

$expectedWitnesses = @(
    'CROSS_SCOPE_IDEMPOTENCY',
    'UNSAFE_INTEGER_ALIAS',
    'ACT_COMPLETION_ID_SUBSTITUTION',
    'INVALID_PROPOSAL_PATH_DIVERGENCE',
    'UNJOURNALED_A0_A1',
    'MULTI_GOLD_GUESSING',
    'RENDER_ID_LEAKAGE',
    'CONFIG_PRECOMPUTED_PACKET',
    'COUNTER_SPLIT',
    'HD_INTERACTION',
    'IMPOSSIBLE_OC_CELL',
    'MISSING_OM_BRANCH_FLIP',
    'PERIODIC_INDEX_AMBIGUITY',
    'INFERENCE_IMPLEMENTATION_MISMATCH'
)
$actualWitnesses = @($state.red_witnesses + $packets.red_witnesses + $measurement.red_witnesses + $inference.red_witnesses)
foreach ($witness in $expectedWitnesses) {
    Assert-True ($actualWitnesses -contains $witness) "Missing r7 red witness: $witness"
}
Assert-True (($actualWitnesses | Sort-Object -Unique).Count -eq 14) 'Red-witness catalog is incomplete or duplicated.'

'PASS: r7 five-artifact normative bundle and fourteen red-witness closures hold.'
