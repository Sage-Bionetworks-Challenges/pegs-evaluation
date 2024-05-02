#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

label: Validate a project submission

requirements:
- class: InlineJavascriptRequirement

inputs:
- id: submissionid
  type: int
- id: challengewiki
  type: string
- id: public
  type: boolean?
- id: admin
  type: string?
- id: synapse_config
  type: File

outputs:
- id: results
  type: File
  outputBinding:
    glob: results.json
- id: status
  type: string
  outputBinding:
    glob: results.json
    loadContents: true
    outputEval: $(JSON.parse(self[0].contents)['submission_status'])
- id: invalid_reasons
  type: string
  outputBinding:
    glob: results.json
    loadContents: true
    outputEval: $(JSON.parse(self[0].contents)['submission_errors'])

baseCommand: challengeutils
arguments:
- prefix: -c
  valueFrom: $(inputs.synapse_config.path)
- valueFrom: validate-project
- valueFrom: $(inputs.submissionid)
- valueFrom: $(inputs.challengewiki)
- prefix: --public
  valueFrom: $(inputs.public)
- prefix: --admin
  valueFrom: $(inputs.admin)
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
