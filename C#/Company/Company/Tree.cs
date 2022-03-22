using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.IO;
using System.Linq;
using Company;
using System.Text.RegularExpressions;
using System.Threading;

namespace Company
{
    public partial class Tree : Form
    {
        string fullpath = "";

        // tùy chọn thư mục hiện tại hay không để thực hiện đếm
        string[] arrFiles = null;
        public Tree()
        {
            InitializeComponent();
        }

        private void Tree_Load(object sender, EventArgs e)
        {
            treeView1.TopNode.Nodes.Clear();
            // lấy ổ đĩa trên máy tính
            string[] drives = Environment.GetLogicalDrives();
            foreach (string var in drives)
            {
                // Thêm node vào treeview
                TreeNode node = new TreeNode(var);
                node.Text = var;
                node.ImageIndex = 1;
                node.SelectedImageIndex = 2;

                treeView1.TopNode.Nodes.Add(node);
            }
        }

        private void treeView1_BeforeSelect(object sender, TreeViewCancelEventArgs e)
        {
            try
            {
                if (e.Node.Text == "My Computer") return;

                // thêm vào treeview
                e.Node.Nodes.Clear();
                fullpath = e.Node.Text;
                TreeNode _node = e.Node.Parent;
                while (_node.Parent != null)
                {
                    if (_node.Parent.Text == "My Computer")
                    {
                        fullpath = _node.Text + fullpath;
                        break;
                    }
                    else
                        fullpath = _node.Text + "\\" + fullpath;

                    _node = _node.Parent;
                }

                string[] folders = Directory.GetDirectories(fullpath);
                foreach (string var in folders)
                {
                    string[] fs = var.Split('\\');
                    // Thêm node vào treeview
                    TreeNode node = new TreeNode(fs[fs.Length - 1]);
                    node.Text = fs[fs.Length - 1];
                    node.ImageIndex = 1;
                    node.SelectedImageIndex = 2;

                    e.Node.Nodes.Add(node);
                }

                // thêm vào view
                listView1.Items.Clear();
                string[] files = Directory.GetFiles(fullpath);

                foreach (string var in files)
                {
                    // Tên của files
                    ListViewItem item = new ListViewItem(Path.GetFileName(var), 0);

                    // Ngày tạo file
                    item.SubItems.Add(File.GetCreationTime(var).ToShortDateString());

                    // Kiểu file
                    string[] type = Path.GetFileName(var).Split('.');
                    /*if (type.Length > 1) item.SubItems.Add(type[type.Length - 1].ToLower());
                    else item.SubItems.Add("File");*/

                    // dung lượng file
                    item.SubItems.Add(String.Format("{0:#,##0.##}", Math.Round((double)new System.IO.FileInfo(var).Length / (double)1024, 0)) + " KB");

                    listView1.Items.Add(item);
                }


                // edit title windows
                Tree.ActiveForm.Text = fullpath;

            }
            catch
            {
            }
        }

        public void result(string path)
        {
            try
            {
                richTextBox1.Text = "";
                double sumSize = 0;

                SearchOption searchOption;
                if (currentDirectory.CheckState == CheckState.Unchecked)
                    searchOption = SearchOption.AllDirectories;
                else
                    searchOption = SearchOption.TopDirectoryOnly;

                arrFiles = Directory.GetFiles(fullpath, "*.*", searchOption)
                    .Where(s => s.ToLower().EndsWith(".pdf") || s.EndsWith(".jpg") || s.EndsWith(".jpeg") || s.EndsWith(".png")).ToArray();

                // trường hợp file không có đuôi sẽ đặt mặc định là File
                List<string> listExtension = new List<string>();

                for (int i = 0; i < arrFiles.Length; i++)
                {
                    string[] type = Path.GetFileName(arrFiles[i]).Split('.');
                    if (type.Length > 1) listExtension.Add(type[type.Length - 1].ToLower());
                    else listExtension.Add("File");
                }

                foreach (string var in listExtension.Distinct().OrderBy(q => q).ToList())
                {
                    string[] arr = (from f in arrFiles where f.ToLower().EndsWith(var) select f).ToArray();

                    double sizeFiles = getSizeFiles(arr);

                    richTextBox1.Text = richTextBox1.Text + String.Format("{0:#,##0.##}", arr.Length) +
                        " files " + var + ": " + String.Format("{0:#,##0.##}", sizeFiles) + " MB\n";

                    sumSize += sizeFiles;
                }

                richTextBox1.Text = richTextBox1.Text + "\n\n\n" + "Tổng :\t" + String.Format("{0:#,##0.##}", sumSize) + " MB";
            }
            catch (Exception) { }
        }

        public double getSizeFiles(string[] folderPath)
        {
            double sum = 0;
            foreach (string var in folderPath)
            {
                sum += new System.IO.FileInfo(var).Length;
            }
            return Math.Round((double)sum / (double)(1024 * 1024), 0);
        }

        private void toolStripMenuItem3_Click(object sender, EventArgs e)
        {
            result(fullpath);
        }

        private void listView1_ColumnClick(object sender, ColumnClickEventArgs e)
        {
            ItemComparer sorter = listView1.ListViewItemSorter as ItemComparer;

            if (sorter == null)
            {
                sorter = new ItemComparer(e.Column);
                sorter.Order = SortOrder.Ascending;
                listView1.ListViewItemSorter = sorter;
            }
            // if clicked column is already the column that is being sorted
            if (e.Column == sorter.Column)
            {
                // Reverse the current sort direction
                if (sorter.Order == SortOrder.Ascending)
                    sorter.Order = SortOrder.Descending;
                else
                    sorter.Order = SortOrder.Ascending;
            }
            else
            {
                // Set the column number that is to be sorted; default to ascending.
                sorter.Column = e.Column;
                sorter.Order = SortOrder.Ascending;
            }
            listView1.Sort();
        }

        private void thaoTacDB_Click(object sender, EventArgs e)
        {
            Company.Home frm = new Home();
            frm.Show();

            this.Hide();
        }

        private void thongKeToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Company.DuAn.BinhPhuoc bp = new Company.DuAn.BinhPhuoc();
            bp.ThongKeSKHDT();
        }

        private void listView1_SelectedIndexChanged(object sender, EventArgs e)
        {
            try
            {
                if (listView1.SelectedItems.Count > 0)
                {
                    System.Diagnostics.Process.Start(Path.Combine(fullpath, listView1.SelectedItems[0].Text));
                }
            }
            catch { }
        }

        private void Tree_FormClosing(object sender, FormClosingEventArgs e)
        {
            Home.form1.Show();
        }

        private void richTextBox1_Click(object sender, EventArgs e)
        {
            // add text in richTextBox1
            result(fullpath);
        }

        private void countPdfStripMenuItem3_Click(object sender, EventArgs e)
        {            
            MessageBox.Show("Có " + String.Format("{0:#,##0.##}", Utils.countPdf((from f in arrFiles where f.ToLower().EndsWith("pdf") select f).ToArray()))
                + " trang pdf", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void renamepdfMenuItem3_Click(object sender, EventArgs e)
        {
            this.Hide();
            Rename rename = new Rename();
            rename.Show();
            
            /*SearchOption searchOption;
            if (currentDirectory.CheckState == CheckState.Unchecked)
                searchOption = SearchOption.AllDirectories;
            else
                searchOption = SearchOption.TopDirectoryOnly;

            string[] pdfFiles = Directory.GetFiles(fullpath, "*.*", searchOption)
                    .Where(s => s.EndsWith(".pdf")).ToArray();*/
        }
    }
}