#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

label: Create a copy of the project submission

requirements:
- class: InlineJavascriptRequirement

inputs:
- id: submissionid
  type: int
- id: admin
  type: string
- id: synapse_config
  type: File
- id: check_validation_finished
  type: boolean?

outputs:
- id: results
  type: File
  outputBinding:
    glob: results.json

baseCommand: challengeutils
arguments:
- prefix: -c
  valueFrom: $(inputs.synapse_config.path)
- valueFrom: archive-project
- valueFrom: $(inputs.submissionid)
- valueFrom: $(inputs.admin)
- prefix: --output
  valueFrom: results.json

hints:
  DockerRequirement:
    dockerPull: sagebionetworks/challengeutils:v4.2.1

s:author:
- class: s:Person
  s:identifier: https://orcid.org/0000-0002-5622-7998
  s:email: verena.chung@sagebase.org
  s:name: Verena Chung

s:codeRepository: https://github.com/Sage-Bionetworks-Challenges/pegs-evaluation

$namespaces:
  s: https://schema.org/
