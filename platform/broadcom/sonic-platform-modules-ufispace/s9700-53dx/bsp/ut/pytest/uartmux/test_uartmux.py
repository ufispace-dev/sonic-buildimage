#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019 UfiSpace Co.,Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest
import sys
from bsp.utility.uartmux_utility import UARTMuxUtility
from bsp.const.const import CPLDConst

@pytest.fixture(scope="session")
def util():
    return UARTMuxUtility()

@pytest.mark.skip(reason="can't read BMC console output")
def test_set_uart_mux(util, capsys):
    
    util.set_uart_mux(CPLDConst.UART_SOURCE_BMC)
    
    sys.stderr.write("world\n")
    print("")

    captured = capsys.readouterr()
    out = captured.out
    err = captured.err
    util.set_uart_mux(CPLDConst.UART_SOURCE_CPU)
    
    assert "UFI" in err
    assert "UFI" in out
    