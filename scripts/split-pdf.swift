import Foundation
import PDFKit

// usage: split-pdf <input.pdf> <output-dir> <base-name> [max-bytes-per-volume]
// 不重新压缩，原页直接搬进新 PDF。默认每卷不超过 24 MiB（Cloudflare Pages 单文件上限 25 MiB）。
// 按页的 dataRepresentation 估算体积，超了就开新卷。

let args = CommandLine.arguments
guard args.count >= 4 else {
    fputs("usage: split-pdf <input.pdf> <output-dir> <base-name> [max-bytes]\n", stderr)
    exit(1)
}

let input = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2])
let base = args[3]
let maxBytes = args.count >= 5 ? (Int(args[4]) ?? 24 * 1024 * 1024) : 24 * 1024 * 1024
try? FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)

guard let doc = PDFDocument(url: input) else {
    fputs("cannot open pdf: \(input.path)\n", stderr)
    exit(2)
}

let total = doc.pageCount
var vol = 1
var cur = PDFDocument()
var curSize = 0
var start = 0

func flush() {
    guard cur.pageCount > 0 else { return }
    let name = "\(base)-v\(vol).pdf"
    let url = outDir.appendingPathComponent(name)
    guard cur.write(to: url) else {
        fputs("write failed: \(name)\n", stderr)
        exit(3)
    }
    let attrs = try? FileManager.default.attributesOfItem(atPath: url.path)
    let size = (attrs?[.size] as? Int) ?? 0
    print("\(name): pages \(start + 1)-\(start + cur.pageCount), \(size) bytes")
}

for i in 0..<total {
    guard let page = doc.page(at: i) else { continue }
    let pageSize = page.dataRepresentation?.count ?? 0
    if cur.pageCount > 0 && curSize + pageSize > maxBytes {
        flush()
        vol += 1
        start = i
        cur = PDFDocument()
        curSize = 0
    }
    cur.insert(page, at: cur.pageCount)
    curSize += pageSize
}
flush()
