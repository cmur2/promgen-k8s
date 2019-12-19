from typing import (Dict)

RelabelingStep = Dict  # pylint: disable=invalid-name

# Basic DSL
# def rc_entry(**kwargs):
#   return kwargs


# Intermediate DSL
def drop(**kwargs) -> RelabelingStep:
  """
  Combines all keyword arguments into a Prometheus relabeling step with action set to 'drop'.
  """
  kwargs['action'] = 'drop'
  return kwargs


def keep(**kwargs) -> RelabelingStep:
  """
  Combines all keyword arguments into a Prometheus relabeling step with action set to 'keep'.
  """
  kwargs['action'] = 'keep'
  return kwargs


def labelmap(**kwargs) -> RelabelingStep:
  """
  Combines all keyword arguments into a Prometheus relabeling step with action set to 'labelmap'.
  """
  kwargs['action'] = 'labelmap'
  return kwargs


def replace(**kwargs) -> RelabelingStep:
  """
  Combines all keyword arguments into a Prometheus relabeling step with action set to 'replace'.
  """
  kwargs['action'] = 'replace'
  return kwargs


# Advanced DSL
def set_value(label_name, value) -> RelabelingStep:
  # replace target with given value unconditionally
  return replace(replacement=value, target_label=label_name)


def copy_value(src_label_name, tgt_label_name) -> RelabelingStep:
  # replace target with source unconditionally
  return replace(source_labels=[src_label_name], target_label=tgt_label_name)


def remove_label(label_name) -> RelabelingStep:
  # set empty value
  return set_value(label_name, '')
