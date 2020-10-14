#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: USER
Email: yli056@e.ntu.edu.sg
Date: 10/12/2020
"""
import click
import requests

from modelci.app import SERVER_HOST, SERVER_PORT
from modelci.hub.init_data import export_model
from modelci.ui import model_view, model_detailed_view
from modelci.utils.misc import remove_dict_null


@click.command()
@click.argument('name', type=click.STRING, required=False)
@click.option(
    '-f', '--framework',
    type=click.Choice(['TensorFlow', 'PyTorch'], case_sensitive=False),
    help='Model framework.'
)
@click.option(
    '-e', '--engine',
    type=click.Choice(['NONE', 'TFS', 'TORCHSCRIPT', 'ONNX', 'TRT', 'TVM', 'CUSTOMIZED'], case_sensitive=False),
    help='Model serving engine.'
)
@click.option('-v', '--version', type=click.INT, help='Model version.')
@click.option('-a', '--all', 'list_all', type=click.BOOL, is_flag=True, help='Show all models.')
@click.option('-q', '--quiet', type=click.BOOL, is_flag=True, help='Only show numeric IDs.')
def models(name, framework, engine, version, list_all, quiet):
    payload = remove_dict_null({'name': name, 'framework': framework, 'engine': engine, 'version': version})
    with requests.get(f'http://{SERVER_HOST}:{SERVER_PORT}/api/v1/model/', params=payload) as r:
        model_list = r.json()
        model_view([model_list], list_all=list_all, quiet=quiet)


@click.group('model')
def commands():
    """
    ModelCI hub for Manage (CURD), convert, diagnose and deploy DL models supported by industrial
    serving systems.
    """
    pass


@commands.command()
@click.option('-n', '--name', type=click.STRING, required=True, help='Model architecture name.')
@click.option(
    '-f', '--framework',
    type=click.Choice(['TensorFlow', 'PyTorch'], case_sensitive=False),
    required=True,
    help='Model framework name.'
)
@click.option(
    '--trt',
    type=click.STRING,
    is_flag=True,
    help='Flag for exporting models served by TensorRT. Please make sure you have TensorRT installed in your machine'
         'before set this flag.'
)
def export(name, framework, trt):
    """
    Export model from PyTorch hub / TensorFlow hub and try convert the model into various format for different serving
    engines.
    """
    export_model(model_name=name, framework=framework, enable_trt=trt)
    exit(0)


@commands.command()
@click.argument('model_id')
def show(model_id):
    """Show a single model."""
    with requests.get(f'http://{SERVER_HOST}:{SERVER_PORT}/api/v1/model/{model_id}') as r:
        model = r.json()
        model_detailed_view(model)
