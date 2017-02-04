# 自分の得意な言語で
# Let's チャレンジ！！
class IslandMap
  attr_accessor :m, :n, :matrix, :lands, :number_of_islands
  attr_accessor :next_tag, :tag_group

  SEA = "0".freeze
  LAND = "1".freeze

  def initialize(m, n)
    self.m, self.n = m, n
    self.matrix = n.times.map do
      gets.split(" ")
    end
    self.number_of_islands = 0
    self.tag_group = {}
    self.next_tag = 0
  end

  def land?(i, j)
    return false if i < 0 || j < 0
    matrix[i][j].is_a?(Integer)
  end

  def tag(x)
    loop do
      return x if x == tag_group[x]
      x = tag_group[x]
    end
  end

  def count
    n.times do |i|
      m.times do |j|
        if matrix[i][j] == LAND
          if land?(i-1, j) && land?(i, j-1) # 北も南も陸地の場合
            # 北と西が同じならば内容をコピー
            if tag(matrix[i-1][j]) == tag(matrix[i][j-1])
              matrix[i][j] = tag(matrix[i-1][j])
            elsif tag(matrix[i-1][j]) < tag(matrix[i][j-1])
              matrix[i][j] = tag(matrix[i-1][j])
              tag_group[tag(matrix[i][j-1])] = tag(matrix[i-1][j])
            elsif matrix[i-1][j] > matrix[i][j-1]
              matrix[i][j] = tag(matrix[i][j-1])
              tag_group[tag(matrix[i-1][j])] = tag(matrix[i][j-1])
            end
          elsif land?(i-1, j)
            matrix[i][j] = tag(matrix[i-1][j])
          elsif land?(i, j-1)
            matrix[i][j] = tag(matrix[i][j-1])
          else
            self.next_tag += 1
            tag_group[next_tag] = next_tag
            matrix[i][j] = next_tag
          end
        end
      end
    end

    tag_group.select{|k, v| k == v}.size
  end
end

m, n = gets.split(" ").map(&:to_i) # m列n行

im = IslandMap.new(m, n)
puts im.count
