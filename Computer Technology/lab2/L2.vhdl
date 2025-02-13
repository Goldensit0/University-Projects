library ieee;
use ieee.std_logic_1164.all;

entity L2 is
  port(
    r1, sc1, p1: in std_logic;
    r2, sc2, p2: in std_logic;
    LED1, LED2: out std_logic
  );
end L2;

-- AND gate
architecture behavior of L2 is
  signal s1, s2: std_logic_vector(1 downto 0);
  signal rsp1, rsp2: std_logic_vector(2 downto 0);
begin
  rsp1 <= r1 & sc1 & p1;
  rsp2 <= r2 & sc2 & p2;
  process(rsp1, rsp2) -- sensitivity list
  begin
    -- ENCODER BLOCK 1
    case rsp1 is
      when "100" => s1 <= "01"; -- rock
      when "010" => s1 <= "10"; -- scissors
      when "001" => s1 <= "11"; -- paper
      when others => s1 <= "00"; -- not pressed or multiple button pressed
    end case;
    -- ENCODER BLOCK 1
    case rsp2 is
      when "100" => s2 <= "01"; -- rock
      when "010" => s2 <= "10"; -- scissors
      when "001" => s2 <= "11"; -- paper
      when others => s2 <= "00"; -- not pressed or multiple button pressed
    end case;
  end process;
  -- RESULTS LOGIC BLOCK
  process(s1, s2)
  begin
    case s1 is
      when "00" =>
        LED1 <= '0'; -- mux to LED1; input "00"
        LED2 <= s2(1) or s2(0); -- mux to LED2; input "00"
      when "01" =>
        LED1 <= s2(1) nand s2(0); -- mux to LED1; input "01"
        LED2 <= s2(0); -- mux to LED2; input "01"
      when "10" =>
        LED1 <= s2(1) or (not s2(0)); -- mux to LED1; input "10"
        LED2 <= s2(1) xor s2(0); -- mux to LED2; input "10"
      when others =>
        LED1 <= (not s2(1)) or s2(0); -- mux to LED1; input "11"
        LED2 <= s2(1); -- mux to LED2; input "11"
    end case;
  end process;
end behavior;
