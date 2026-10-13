# MBCX-01 r11 physical harness requirement

Status: **required external prerequisite; not implemented by the no-paid r11 bundle**

The Python `baseline_receipt_rows()` function emits synthetic fixtures only. Those fixtures test the evaluator's arithmetic and rejection behavior; they are not OS evidence and must never be used as a candidate pass record.

Before any candidate may pass the physical stage, a separately governed Windows harness must:

1. create the candidate root suspended;
2. create a named Job Object, associate its completion port while inactive, disable both breakaway modes, assign the root, then resume it;
3. deny network egress and external compute;
4. retain process identity evidence for every job member, including terminated members;
5. wait for active-process-zero, drain the completion port, and make a final `QueryInformationJobObject(JobObjectBasicAndIoAccountingInformation)` query;
6. collect job-wide CPU and I/O, peak committed memory, and monotonic elapsed time;
7. use one pinned retired-instruction backend whose report binds process start keys/PIDs to job membership;
8. sign each canonical receipt with a pinned public-key identity whose private key is not available to the candidate or evaluator; and
9. run all 100 registered H-D-F cells for one candidate/generator identity.

The r11 verifier intentionally reports `PHYSICAL_HARNESS_UNAVAILABLE`, and the governing stage order treats that as `DESIGN_OR_IMPLEMENTATION_FAIL`, until such a harness and trust root are pinned. This is a pre-experiment engineering gate, not a paid/provider/model call and not experimental evidence.

Primary platform references:

- https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects
- https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port
- https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class
