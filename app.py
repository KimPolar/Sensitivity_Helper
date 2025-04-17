import wx
import math

class PSAPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout()

    def layout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, label="🧪 PSA 감도 조정")
        title.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(title, 0, wx.ALL, 10)

        self.input_sense = wx.TextCtrl(self, value="50.0")
        vbox.Add(wx.StaticText(self, label="초기 감도 (예: 50):"), 0, wx.LEFT | wx.TOP, 10)
        vbox.Add(self.input_sense, 0, wx.EXPAND | wx.ALL, 10)

        btn_start = wx.Button(self, label="PSA 테스트 시작")
        btn_start.Bind(wx.EVT_BUTTON, self.on_psa_start)
        vbox.Add(btn_start, 0, wx.ALL | wx.CENTER, 10)

        self.SetSizer(vbox)

    def on_psa_start(self, event):
        try:
            initial_sense = float(self.input_sense.GetValue())
            if initial_sense <= 0:
                raise ValueError("감도는 0보다 커야 합니다.")
            self.psa_step(initial_sense, 1)
        except ValueError:
            wx.MessageBox("유효한 숫자를 입력해주세요! (예: 1.25)", "입력 오류", wx.OK | wx.ICON_ERROR)

    def psa_step(self, sense, step):
        if step in [1, 2]:
            low = sense * 0.5
            high = sense * 1.5
        elif step in [3, 4, 5, 6]:
            mul = (step + 3) * 0.1
            low = sense * mul
            high = sense * (2 - mul)
        elif step == 7:
            low = sense * 0.95
            high = sense * 1.05
        else:
            return

        low = round(low, 2)
        high = round(high, 2)

        dlg = wx.MessageDialog(self,
            f"현재 감도: {sense:.2f}\n\n"
            f"🔽 Lower: {low}\n"
            f"🔼 Higher: {high}", f"PSA 단계 {step}",
            wx.YES_NO | wx.ICON_QUESTION)

        dlg.SetYesNoLabels("Lower", "Higher")
        result = dlg.ShowModal()
        dlg.Destroy()

        if result == wx.ID_YES:
            next_sense = round((sense + low) / 2, 2)
        else:
            next_sense = round((sense + high) / 2, 2)

        if step == 7:
            wx.MessageBox(f"🎉 최종 추천 감도: {next_sense}", "PSA 완료", wx.OK | wx.ICON_INFORMATION)
            self.input_sense.SetValue(str(next_sense))
        else:
            self.psa_step(next_sense, step + 1)


class DPIConvertPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout()

    def layout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, label="🎯 DPI 감도 변환")
        title.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(title, 0, wx.ALL, 10)

        self.sense_txt = wx.TextCtrl(self, value="1.0")
        self.old_dpi_txt = wx.TextCtrl(self, value="800")
        self.new_dpi_txt = wx.TextCtrl(self, value="1600")
        self.result_lbl = wx.StaticText(self, label="")

        grid = wx.FlexGridSizer(3, 2, 10, 10)
        grid.AddMany([
            (wx.StaticText(self, label="현재 감도:"), 0, wx.ALIGN_CENTER_VERTICAL),
            (self.sense_txt, 1, wx.EXPAND),

            (wx.StaticText(self, label="기존 DPI:"), 0, wx.ALIGN_CENTER_VERTICAL),
            (self.old_dpi_txt, 1, wx.EXPAND),

            (wx.StaticText(self, label="새 DPI:"), 0, wx.ALIGN_CENTER_VERTICAL),
            (self.new_dpi_txt, 1, wx.EXPAND),
        ])
        grid.AddGrowableCol(1, 1)

        vbox.Add(grid, 0, wx.EXPAND | wx.ALL, 10)

        btn_convert = wx.Button(self, label="DPI 변환 실행")
        btn_convert.Bind(wx.EVT_BUTTON, self.on_convert)
        vbox.Add(btn_convert, 0, wx.ALL | wx.CENTER, 10)
        vbox.Add(self.result_lbl, 0, wx.LEFT | wx.RIGHT, 10)

        self.SetSizer(vbox)

    def on_convert(self, event):
        try:
            sense = float(self.sense_txt.GetValue())
            old_dpi = int(self.old_dpi_txt.GetValue())
            new_dpi = int(self.new_dpi_txt.GetValue())
            result = sense + 15 * math.log2(old_dpi / new_dpi)
            self.result_lbl.SetLabel(f"🔁 변환된 감도: {round(result, 2)}")
        except ValueError:
            wx.MessageBox("숫자를 정확히 입력해주세요!", "입력 오류", wx.OK | wx.ICON_ERROR)

class SensitivityApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="🎮 감도 조정 도구", size=(500, 380))
        self.notebook = wx.Notebook(self)

        self.psa_panel = PSAPanel(self.notebook)
        self.dpi_panel = DPIConvertPanel(self.notebook)

        self.notebook.AddPage(self.psa_panel, "PSA 감도 조정")
        self.notebook.AddPage(self.dpi_panel, "DPI 감도 변환")

        self.Centre()
        self.Show()

if __name__ == '__main__':
    app = wx.App(False)
    SensitivityApp()
    app.MainLoop()
